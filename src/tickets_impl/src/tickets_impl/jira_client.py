"""Low-level Jira client implementation."""

from __future__ import annotations

import os
from datetime import datetime
from uuid import UUID

import httpx

from tickets_api.client import (
    Comment,
    Ticket,
    TicketPriority,
    TicketStatus,
)
from tickets_impl.config import load_config
from tickets_impl.oauth import JiraOAuth


class JiraClient:
    """Client responsible for communicating with Jira REST API."""

    def __init__(self) -> None:
        self._config = load_config()
        self._oauth = JiraOAuth()

        project_key = os.getenv("JIRA_PROJECT_KEY")
        if not project_key:
            raise RuntimeError("Missing required environment variable: JIRA_PROJECT_KEY")

        self._project_key = project_key

    async def create_ticket(
        self,
        *,
        title: str,
        description: str,
        reporter: str,
        priority: TicketPriority,
        assignee: str | None,
    ) -> Ticket:
        """Create a Jira issue and return it as a Ticket domain object."""
        access_token = await self._oauth.get_access_token()

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/issue"
        )

        payload = {
            "fields": {
                "project": {"key": self._project_key},
                "summary": title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}],
                        }
                    ],
                },
                "issuetype": {"name": "Task"},
                "priority": {"name": priority.name.capitalize()},
            }
        }

        if assignee:
            payload["fields"]["assignee"] = {"id": assignee}

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)

        response.raise_for_status()
        data = response.json()

        now = datetime.utcnow()

        return Ticket(
            id=UUID(data["id"]),
            title=title,
            description=description,
            status=TicketStatus.OPEN,
            priority=priority,
            reporter=reporter,
            assignee=assignee,
            created_at=now,
            updated_at=now,
        )

    async def get_ticket(self, *, ticket_id) -> Ticket | None:
        """Retrieve a Jira issue by ID and return it as a Ticket."""
        access_token = await self._oauth.get_access_token()

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/issue/{ticket_id}"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        data = response.json()
        fields = data["fields"]

        description_text = ""
        if fields.get("description"):
            content = fields["description"].get("content", [])
            if content and content[0].get("content"):
                description_text = content[0]["content"][0].get("text", "")

        now = datetime.utcnow()

        return Ticket(
            id=UUID(data["id"]),
            title=fields.get("summary", ""),
            description=description_text,
            status=TicketStatus(fields["status"]["name"].lower()),
            priority=TicketPriority(fields["priority"]["name"].lower()),
            reporter=fields["reporter"]["displayName"],
            assignee=(
                fields["assignee"]["accountId"]
                if fields.get("assignee")
                else None
            ),
            created_at=now,
            updated_at=now,
        )

    async def list_tickets(
        self,
        *,
        status: TicketStatus | None,
        assignee: str | None,
        reporter: str | None,
        limit: int,
        offset: int,
    ) -> list[Ticket]:
        """Search Jira issues and return them as Ticket objects."""
        access_token = await self._oauth.get_access_token()

        jql_parts: list[str] = []

        if status:
            jql_parts.append(f'status = "{status.name.capitalize()}"')
        if assignee:
            jql_parts.append(f'assignee = "{assignee}"')
        if reporter:
            jql_parts.append(f'reporter = "{reporter}"')

        jql = " AND ".join(jql_parts) if jql_parts else ""

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/search"
        )

        params = {"jql": jql, "maxResults": limit, "startAt": offset}

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=headers, params=params)

        response.raise_for_status()
        data = response.json()

        now = datetime.utcnow()
        tickets: list[Ticket] = []

        for issue in data.get("issues", []):
            fields = issue["fields"]

            description_text = ""
            if fields.get("description"):
                content = fields["description"].get("content", [])
                if content and content[0].get("content"):
                    description_text = content[0]["content"][0].get("text", "")

            tickets.append(
                Ticket(
                    id=UUID(issue["id"]),
                    title=fields.get("summary", ""),
                    description=description_text,
                    status=TicketStatus(fields["status"]["name"].lower()),
                    priority=TicketPriority(fields["priority"]["name"].lower()),
                    reporter=fields["reporter"]["displayName"],
                    assignee=(
                        fields["assignee"]["accountId"]
                        if fields.get("assignee")
                        else None
                    ),
                    created_at=now,
                    updated_at=now,
                )
            )

        return tickets

    async def update_ticket(
        self,
        *,
        ticket_id,
        title: str | None,
        description: str | None,
        status: TicketStatus | None,
        priority: TicketPriority | None,
        assignee: str | None,
    ) -> Ticket | None:
        """Update mutable fields of a Jira issue."""
        access_token = await self._oauth.get_access_token()

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/issue/{ticket_id}"
        )

        fields: dict[str, object] = {}

        if title is not None:
            fields["summary"] = title
        if description is not None:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }
        if priority is not None:
            fields["priority"] = {"name": priority.name.capitalize()}
        if assignee is not None:
            fields["assignee"] = {"id": assignee}

        if not fields:
            return await self.get_ticket(ticket_id=ticket_id)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(url, json={"fields": fields}, headers=headers)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return await self.get_ticket(ticket_id=ticket_id)

    async def delete_ticket(self, *, ticket_id) -> bool:
        """Delete a Jira issue."""
        access_token = await self._oauth.get_access_token()

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/issue/{ticket_id}"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(url, headers=headers)

        if response.status_code == 404:
            return False

        response.raise_for_status()
        return True

    async def add_comment(
        self,
        *,
        ticket_id,
        author: str,
        content: str,
    ) -> Comment | None:
        """Add a comment to a Jira issue."""
        access_token = await self._oauth.get_access_token()

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/issue/{ticket_id}/comment"
        )

        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": content}],
                    }
                ],
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        data = response.json()

        return Comment(
            id=UUID(data["id"]),
            ticket_id=UUID(ticket_id),
            author=author,
            content=content,
            created_at=datetime.utcnow(),
        )

    async def get_ticket_comments(self, *, ticket_id) -> list[Comment]:
        """Retrieve all comments for a Jira issue."""
        access_token = await self._oauth.get_access_token()

        url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3/issue/{ticket_id}/comment"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 404:
            return []

        response.raise_for_status()
        data = response.json()

        comments: list[Comment] = []

        for item in data.get("comments", []):
            body = item.get("body", {})
            text = ""

            content = body.get("content", [])
            if content and content[0].get("content"):
                text = content[0]["content"][0].get("text", "")

            comments.append(
                Comment(
                    id=UUID(item["id"]),
                    ticket_id=UUID(ticket_id),
                    author=item["author"]["displayName"],
                    content=text,
                    created_at=datetime.fromisoformat(
                        item["created"].replace("Z", "+00:00")
                    ),
                )
            )

        return comments

    async def transition_status(
        self,
        *,
        ticket_id,
        status: TicketStatus,
    ) -> Ticket | None:
        """Transition a Jira issue to a new status."""
        access_token = await self._oauth.get_access_token()

        base_url = (
            f"https://api.atlassian.com/ex/jira/"
            f"{self._config.jira_cloud_id}/rest/api/3"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            transitions_resp = await client.get(
                f"{base_url}/issue/{ticket_id}/transitions",
                headers=headers,
            )

        if transitions_resp.status_code == 404:
            return None

        transitions_resp.raise_for_status()
        transitions_data = transitions_resp.json()

        desired_status = status.name.replace("_", " ").lower()
        transition_id: str | None = None

        for transition in transitions_data.get("transitions", []):
            if transition["to"]["name"].lower() == desired_status:
                transition_id = transition["id"]
                break

        if not transition_id:
            raise RuntimeError(
                f"No valid transition found for status '{status.name}'"
            )

        async with httpx.AsyncClient(timeout=30) as client:
            transition_resp = await client.post(
                f"{base_url}/issue/{ticket_id}/transitions",
                headers=headers,
                json={"transition": {"id": transition_id}},
            )

        transition_resp.raise_for_status()
        return await self.get_ticket(ticket_id=ticket_id)
