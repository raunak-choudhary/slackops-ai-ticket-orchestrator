# src/jira_impl/tests/test_ticket_impl_smoke.py
"""Smoke tests for JiraTicketClient mapping (no network)."""

from __future__ import annotations

from jira_impl.impl import JiraTicketClient
from jira_impl.jira_client import JiraIssue
from tickets_api.client import TicketStatus


class _FakeJiraClient:
    def create_issue(
        self,
        *,
        project_key: str,
        summary: str,
        description: str,
        assignee_account_id: str | None,
    ) -> JiraIssue:
        _ = (project_key, assignee_account_id)
        return JiraIssue(
            key="PROJ-1",
            summary=summary,
            description=description,
            status_name="To Do",
            assignee_account_id=assignee_account_id,
        )

    def get_issue(self, issue_key: str) -> JiraIssue:
        if issue_key == "MISSING-1":
            raise KeyError(issue_key)
        return JiraIssue(key=issue_key, summary="S", description="D", status_name="In Progress", assignee_account_id=None)

    def search_issues(self, *, jql: str, max_results: int = 25) -> list[JiraIssue]:
        _ = (jql, max_results)
        return [
            JiraIssue(key="PROJ-2", summary="A", description="B", status_name="Done", assignee_account_id=None),
            JiraIssue(key="PROJ-3", summary="C", description="D", status_name="To Do", assignee_account_id="acct-1"),
        ]

    def update_issue_summary(self, *, issue_key: str, summary: str) -> JiraIssue:
        return JiraIssue(key=issue_key, summary=summary, description="D", status_name="To Do", assignee_account_id=None)

    def delete_issue(self, issue_key: str) -> bool:
        return issue_key != "NOPE-1"


def _make_client_with_fake_jira() -> JiraTicketClient:
    client = object.__new__(JiraTicketClient)
    client._project_key = "PROJ"  # type: ignore[attr-defined]
    client._jira = _FakeJiraClient()  # type: ignore[attr-defined]
    return client  # type: ignore[return-value]


def test_create_get_search_update_delete_smoke() -> None:
    client = _make_client_with_fake_jira()

    created = client.create_ticket("Title", "Desc", assignee="acct-1")
    assert created.id == "PROJ-1"
    assert created.status == TicketStatus.OPEN

    found = client.get_ticket("PROJ-99")
    assert found is not None
    assert found.id == "PROJ-99"
    assert found.status == TicketStatus.IN_PROGRESS

    missing = client.get_ticket("MISSING-1")
    assert missing is None

    results = client.search_tickets(query="hello", status=TicketStatus.OPEN)
    assert [t.id for t in results] == ["PROJ-2", "PROJ-3"]
    assert results[0].status == TicketStatus.CLOSED
    assert results[1].assignee == "acct-1"

    updated = client.update_ticket("PROJ-9", title="New", status=TicketStatus.CLOSED)
    assert updated.id == "PROJ-9"
    assert updated.title == "New"

    assert client.delete_ticket("PROJ-10") is True
    assert client.delete_ticket("NOPE-1") is False
