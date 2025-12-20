"""Dependency injection tests for tickets_api."""

from __future__ import annotations

import pytest

import tickets_api.client as tickets_client
from tickets_api.client import Ticket, TicketInterface, TicketStatus


class DummyTicket(Ticket):
    """Minimal concrete Ticket implementation for DI tests."""

    def __init__(self) -> None:
        """Initialize a dummy ticket."""
        self._id = "1"

    @property
    def id(self) -> str:
        """Return the ticket ID."""
        return self._id

    @property
    def title(self) -> str:
        """Return the ticket title."""
        return "dummy"

    @property
    def description(self) -> str:
        """Return the ticket description."""
        return "dummy"

    @property
    def status(self) -> TicketStatus:
        """Return the ticket status."""
        return TicketStatus.OPEN

    @property
    def assignee(self) -> str | None:
        """Return the ticket assignee."""
        return None


class DummyTicketService(TicketInterface):
    """Minimal concrete TicketInterface implementation for DI tests."""

    def create_ticket(
        self,
        title: str,
        description: str,
        assignee: str | None = None,
    ) -> Ticket:
        """Create a dummy ticket."""
        return DummyTicket()

    def get_ticket(self, ticket_id: str) -> Ticket | None:
        """Return a dummy ticket by ID."""
        return DummyTicket()

    def search_tickets(
        self,
        query: str | None = None,
        status: TicketStatus | None = None,
    ) -> list[Ticket]:
        """Search for tickets."""
        return []

    def update_ticket(
        self,
        ticket_id: str,
        status: TicketStatus | None = None,
        title: str | None = None,
    ) -> Ticket:
        """Update a ticket."""
        return DummyTicket()

    def delete_ticket(self, ticket_id: str) -> bool:
        """Delete a ticket."""
        return True


@pytest.mark.unit
def test_get_client_can_be_monkey_patched(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """get_client should return the injected implementation."""
    service = DummyTicketService()

    monkeypatch.setattr(tickets_client, "get_client", lambda: service)

    assert tickets_client.get_client() is service
