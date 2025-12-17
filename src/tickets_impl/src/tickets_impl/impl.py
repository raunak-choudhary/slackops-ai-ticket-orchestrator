"""Jira-backed TicketServiceAPI implementation."""

from __future__ import annotations

from tickets_api.client import (
    Comment,
    Ticket,
    TicketPriority,
    TicketServiceAPI,
    TicketStatus,
)
from tickets_impl.jira_client import JiraClient


class TicketImpl(TicketServiceAPI):
    """Concrete TicketServiceAPI backed by Jira."""

    def __init__(self) -> None:
        self._client = JiraClient()

    async def create_ticket(
        self,
        *,
        title: str,
        description: str,
        reporter: str,
        priority: TicketPriority,
        assignee: str | None,
    ) -> Ticket:
        return await self._client.create_ticket(
            title=title,
            description=description,
            reporter=reporter,
            priority=priority,
            assignee=assignee,
        )

    async def get_ticket(self, ticket_id) -> Ticket | None:
        return await self._client.get_ticket(ticket_id=ticket_id)

    async def list_tickets(
        self,
        *,
        status: TicketStatus | None = None,
        assignee: str | None = None,
        reporter: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Ticket]:
        return await self._client.list_tickets(
            status=status,
            assignee=assignee,
            reporter=reporter,
            limit=limit,
            offset=offset,
        )

    async def update_ticket(
        self,
        *,
        ticket_id,
        title: str | None = None,
        description: str | None = None,
        status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        assignee: str | None = None,
    ) -> Ticket | None:
        return await self._client.update_ticket(
            ticket_id=ticket_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            assignee=assignee,
        )

    async def delete_ticket(self, ticket_id) -> bool:
        return await self._client.delete_ticket(ticket_id=ticket_id)

    async def add_comment(
        self,
        *,
        ticket_id,
        author: str,
        content: str,
    ) -> Comment | None:
        return await self._client.add_comment(
            ticket_id=ticket_id,
            author=author,
            content=content,
        )

    async def get_ticket_comments(self, ticket_id) -> list[Comment]:
        return await self._client.get_ticket_comments(ticket_id=ticket_id)

    async def transition_status(
        self,
        *,
        ticket_id,
        status: TicketStatus,
    ) -> Ticket | None:
        return await self._client.transition_status(
            ticket_id=ticket_id,
            status=status,
        )
