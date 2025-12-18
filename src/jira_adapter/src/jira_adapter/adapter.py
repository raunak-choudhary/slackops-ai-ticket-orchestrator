"""Service-backed Jira adapter implementation.

Implements the TicketInterface by delegating all operations to the
Jira FastAPI service via the auto-generated HTTP client.
"""

from __future__ import annotations

from tickets_api.client import Ticket, TicketInterface, TicketStatus
from tickets_service_api_client import Client

from tickets_service_api_client.api.default.create_ticket_tickets_post import (
    sync as create_ticket,
)
from tickets_service_api_client.api.default.get_ticket_tickets_ticket_id_get import (
    sync as get_ticket,
)
from tickets_service_api_client.api.default.list_tickets_tickets_get import (
    sync as list_tickets,
)

from tickets_service_api_client.models.ticket_in import TicketIn
from tickets_service_api_client.models.ticket_out import TicketOut


# -------------------------
# Domain Ticket Wrapper
# -------------------------


class JiraServiceTicket(Ticket):
    """Concrete Ticket implementation backed by jira_service responses."""

    def __init__(self, dto: TicketOut) -> None:
        self._dto = dto

    @property
    def id(self) -> str:
        return self._dto.id

    @property
    def title(self) -> str:
        return self._dto.title

    @property
    def description(self) -> str:
        return self._dto.description

    @property
    def status(self) -> TicketStatus:
        return TicketStatus(self._dto.status)

    @property
    def assignee(self) -> str | None:
        return self._dto.assignee


# -------------------------
# Adapter Implementation
# -------------------------


class JiraServiceTicketClient(TicketInterface):
    """TicketInterface implementation backed by jira_service."""

    def __init__(self, base_url: str) -> None:
        self._client = Client(base_url=base_url)

    def create_ticket(
        self,
        title: str,
        description: str,
        assignee: str | None = None,
    ) -> Ticket:
        try:
            dto = create_ticket(
                client=self._client,
                body=TicketIn(
                    title=title,
                    description=description,
                ),
            )
            return JiraServiceTicket(dto)
        except Exception as exc:  # noqa: BLE001
            raise ConnectionError(
                "Failed to create ticket via Jira service"
            ) from exc

    def get_ticket(self, ticket_id: str) -> Ticket | None:
        try:
            dto = get_ticket(
                ticket_id=ticket_id,
                client=self._client,
            )
            if dto is None:
                return None
            return JiraServiceTicket(dto)
        except Exception as exc:  # noqa: BLE001
            raise ConnectionError(
                "Failed to fetch ticket via Jira service"
            ) from exc

    def search_tickets(
        self,
        query: str | None = None,
        status: TicketStatus | None = None,
    ) -> list[Ticket]:
        try:
            response = list_tickets(
                client=self._client,
                query=query,
                status=status.value if status else None,
            )
            return [JiraServiceTicket(t) for t in response.tickets]
        except Exception as exc:  # noqa: BLE001
            raise ConnectionError(
                "Failed to list tickets via Jira service"
            ) from exc

    def update_ticket(
        self,
        ticket_id: str,
        status: TicketStatus | None = None,
        title: str | None = None,
    ) -> Ticket:
        """Update a ticket.

        NOTE:
        The Jira service does not currently expose an update endpoint.
        This method is intentionally unimplemented.
        """
        raise NotImplementedError(
            "update_ticket is not supported by the Jira service API yet"
        )

    def delete_ticket(self, ticket_id: str) -> bool:
        """Delete a ticket.

        NOTE:
        The Jira service does not currently expose a delete endpoint.
        """
        raise NotImplementedError(
            "delete_ticket is not supported by the Jira service API yet"
        )
