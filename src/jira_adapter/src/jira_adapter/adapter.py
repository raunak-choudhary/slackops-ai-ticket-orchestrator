"""Service-backed Jira adapter implementation.

Implements the TicketInterface by delegating all operations to the
Jira FastAPI service via the auto-generated HTTP client.

IMPORTANT:
- Base URL MUST come from env var: JIRA_SERVICE_BASE_URL
- No hardcoded localhost values (deployment-safe)
"""

from __future__ import annotations

import os

from tickets_api.client import Ticket, TicketInterface, TicketStatus, bind_client
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


class JiraServiceTicketClient(TicketInterface):
    """TicketInterface implementation backed by jira_service."""

    def __init__(self, base_url: str) -> None:
        base_url = base_url.rstrip("/")
        if not base_url:
            raise RuntimeError("JIRA_SERVICE_BASE_URL is empty")
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
                body=TicketIn(title=title, description=description),
            )

            # Generated client may return None even on 201; verify via list.
            if dto is not None:
                return JiraServiceTicket(dto)

            response = list_tickets(client=self._client)
            tickets = getattr(response, "tickets", None) if response else None
            if not tickets:
                raise RuntimeError("Ticket create returned None and list is empty")

            return JiraServiceTicket(tickets[-1])

        except Exception as exc:  # noqa: BLE001
            raise ConnectionError("Failed to create ticket via Jira service") from exc

    def get_ticket(self, ticket_id: str) -> Ticket | None:
        try:
            dto = get_ticket(ticket_id=ticket_id, client=self._client)
            return JiraServiceTicket(dto) if dto else None
        except Exception as exc:  # noqa: BLE001
            raise ConnectionError("Failed to fetch ticket via Jira service") from exc

    def search_tickets(
        self,
        query: str | None = None,
        status: TicketStatus | None = None,
    ) -> list[Ticket]:
        _ = query
        _ = status
        try:
            response = list_tickets(client=self._client)
            tickets = getattr(response, "tickets", None) if response else None
            if not tickets:
                return []
            return [JiraServiceTicket(t) for t in tickets]
        except Exception as exc:  # noqa: BLE001
            raise ConnectionError("Failed to list tickets via Jira service") from exc

    def update_ticket(self, *args, **kwargs) -> Ticket:
        raise NotImplementedError(
            "update_ticket is not supported by the Jira service API yet"
        )

    def delete_ticket(self, *args, **kwargs) -> bool:
        raise NotImplementedError(
            "delete_ticket is not supported by the Jira service API yet"
        )


# -------------------------
# ENV-BASED SINGLETON BIND
# -------------------------

_singleton: JiraServiceTicketClient | None = None


def _get_service_base_url() -> str:
    base_url = os.getenv("JIRA_SERVICE_BASE_URL")
    if not base_url:
        raise RuntimeError("Missing required env var: JIRA_SERVICE_BASE_URL")
    return base_url


def get_singleton() -> JiraServiceTicketClient:
    global _singleton
    if _singleton is None:
        _singleton = JiraServiceTicketClient(base_url=_get_service_base_url())
    return _singleton


# Bind on import using env var (deployment-safe)
bind_client(get_singleton())
