# src/jira_impl/src/jira_impl/jira_client.py
"""Low-level Jira REST client (HTTP + Jira-specific payload shapes only)."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True, slots=True)
class JiraIssue:
    """Minimal Jira issue representation used by jira_impl."""

    key: str
    summary: str
    description: str
    status_name: str
    assignee_account_id: str | None


def _basic_auth_value(email: str, api_token: str) -> str:
    """Return Basic auth header value for Jira API token auth."""
    raw = f"{email}:{api_token}".encode("utf-8")
    return f"Basic {base64.b64encode(raw).decode('utf-8')}"


def _extract_description_text(value: Any) -> str:
    """Best-effort extraction of a plain-text description from Jira.

    Jira Cloud often uses Atlassian Document Format (ADF).
    This function is intentionally conservative and never raises on unknown shapes.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        content = value.get("content")
        if not isinstance(content, list):
            return ""
        parts: list[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            inner = block.get("content")
            if not isinstance(inner, list):
                continue
            for node in inner:
                if isinstance(node, dict) and isinstance(node.get("text"), str):
                    parts.append(node["text"])
        return "\n".join([p for p in parts if p.strip()])

    return ""


def _to_adf(text: str) -> dict[str, Any]:
    """Convert plain text into a minimal ADF document."""
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": text or ""}],
            }
        ],
    }


class JiraClient:
    """HTTP client for Jira Cloud REST API v3.

    This layer should not expose tickets_api concepts; it deals in Jira issues.
    """

    def __init__(
        self,
        *,
        base_url: str,
        email: str,
        api_token: str,
        timeout_seconds: float = 20.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": _basic_auth_value(email, api_token),
        }
        self._timeout = httpx.Timeout(timeout_seconds)

    def _request(self, method: str, path: str, json_body: dict[str, Any] | None = None) -> httpx.Response:
        """Make a Jira API request.

        Raises:
            ConnectionError: On network/transport failures.
        """
        url = f"{self._base_url}{path}"
        try:
            with httpx.Client(timeout=self._timeout) as client:
                return client.request(method=method, url=url, headers=self._headers, json=json_body)
        except httpx.RequestError as exc:
            raise ConnectionError(f"Jira request failed: {exc}") from exc

    def create_issue(
        self,
        *,
        project_key: str,
        summary: str,
        description: str,
        assignee_account_id: str | None,
    ) -> JiraIssue:
        """Create a Jira issue (Task)."""
        payload: dict[str, Any] = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": _to_adf(description),
                "issuetype": {"name": "Task"},
            }
        }
        if assignee_account_id:
            payload["fields"]["assignee"] = {"accountId": assignee_account_id}

        resp = self._request("POST", "/rest/api/3/issue", json_body=payload)
        if resp.status_code >= 400:
            raise RuntimeError(f"Jira create_issue failed: HTTP {resp.status_code}: {resp.text}")

        data = resp.json()
        key = str(data.get("key") or "")
        if not key:
            raise RuntimeError("Jira create_issue returned no issue key")

        return self.get_issue(key)

    def get_issue(self, issue_key: str) -> JiraIssue:
        """Get a Jira issue by key."""
        resp = self._request("GET", f"/rest/api/3/issue/{issue_key}")
        if resp.status_code == 404:
            raise KeyError(issue_key)
        if resp.status_code >= 400:
            raise RuntimeError(f"Jira get_issue failed: HTTP {resp.status_code}: {resp.text}")

        data = resp.json()
        fields = data.get("fields", {}) if isinstance(data, dict) else {}

        summary = str(fields.get("summary") or "")
        description = _extract_description_text(fields.get("description"))

        status_name = ""
        status_field = fields.get("status")
        if isinstance(status_field, dict):
            status_name = str(status_field.get("name") or "")

        assignee_account_id: str | None = None
        assignee_field = fields.get("assignee")
        if isinstance(assignee_field, dict) and isinstance(assignee_field.get("accountId"), str):
            assignee_account_id = assignee_field["accountId"]

        return JiraIssue(
            key=str(data.get("key") or issue_key),
            summary=summary,
            description=description,
            status_name=status_name,
            assignee_account_id=assignee_account_id,
        )

    def search_issues(self, *, jql: str, max_results: int = 25) -> list[JiraIssue]:
        """Search Jira issues by JQL."""
        payload = {"jql": jql, "maxResults": max_results}
        resp = self._request("POST", "/rest/api/3/search", json_body=payload)
        if resp.status_code >= 400:
            raise RuntimeError(f"Jira search failed: HTTP {resp.status_code}: {resp.text}")

        data = resp.json()
        issues = data.get("issues", []) if isinstance(data, dict) else []
        results: list[JiraIssue] = []
        for issue in issues:
            if not isinstance(issue, dict):
                continue
            key = issue.get("key")
            if isinstance(key, str) and key:
                # Fetch full issue to normalize fields consistently.
                try:
                    results.append(self.get_issue(key))
                except KeyError:
                    continue
        return results

    def update_issue_summary(self, *, issue_key: str, summary: str) -> JiraIssue:
        """Update the issue summary/title."""
        payload = {"fields": {"summary": summary}}
        resp = self._request("PUT", f"/rest/api/3/issue/{issue_key}", json_body=payload)
        if resp.status_code == 404:
            raise KeyError(issue_key)
        if resp.status_code >= 400:
            raise RuntimeError(f"Jira update failed: HTTP {resp.status_code}: {resp.text}")
        return self.get_issue(issue_key)

    def delete_issue(self, issue_key: str) -> bool:
        """Delete an issue by key."""
        resp = self._request("DELETE", f"/rest/api/3/issue/{issue_key}")
        if resp.status_code == 404:
            return False
        if resp.status_code >= 400:
            raise RuntimeError(f"Jira delete failed: HTTP {resp.status_code}: {resp.text}")
        return True
