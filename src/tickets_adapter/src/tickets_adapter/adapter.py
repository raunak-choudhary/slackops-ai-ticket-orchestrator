"""Service-backed adapter for tickets API (Slack-style direct adapter)."""

from __future__ import annotations

from tickets_api.client import Ticket

from tickets_service_api_client import Client as HttpClient
from tickets_service_api_client.api.default import (
    create_ticket_tickets_post,
    get_ticket_tickets_ticket_id_get,
    list_tickets_tickets_get,
)
from tickets_service_api_client.models import TicketIn, TicketOut, TicketsResponse


class TicketsServiceAdapter:
    """Direct adapter that calls the Tickets HTTP service via generated client."""

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self._client = HttpClient(base_url=base_url)

    def get_ticket(self, ticket_id: str) -> Ticket:
        resp: TicketOut = get_ticket_tickets_ticket_id_get.sync(
            client=self._client,
            ticket_id=ticket_id,
        )
        return Ticket(
            id=resp.id,
            title=resp.title,
            description=resp.description,
            status=resp.status,
        )

    def create_ticket(
        self,
        title: str,
        description: str | None = None,
    ) -> Ticket:
        body = TicketIn(title=title, description=description)
        resp: TicketOut = create_ticket_tickets_post.sync(
            client=self._client,
            json_body=body,
        )
        return Ticket(
            id=resp.id,
            title=resp.title,
            description=resp.description,
            status=resp.status,
        )

    def list_tickets(self) -> list[Ticket]:
        resp: TicketsResponse = list_tickets_tickets_get.sync(
            client=self._client
        )
        return [
            Ticket(
                id=t.id,
                title=t.title,
                description=t.description,
                status=t.status,
            )
            for t in resp.tickets
        ]
