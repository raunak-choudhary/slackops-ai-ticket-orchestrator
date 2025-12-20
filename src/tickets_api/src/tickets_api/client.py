"""Abstract interfaces for Ticketing APIs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import StrEnum


class TicketStatus(StrEnum):
    """Enumeration of possible ticket statuses."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class Ticket(ABC):
    """Abstract representation of a ticket."""
    @property
    @abstractmethod
    def id(self) -> str:
        """Return the unique ticket identifier."""
        ...

    @property
    @abstractmethod
    def title(self) -> str:
        """Return the unique ticket identifier."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the unique ticket identifier."""
        ...

    @property
    @abstractmethod
    def status(self) -> TicketStatus:
        """Return the unique ticket identifier."""
        ...

    @property
    @abstractmethod
    def assignee(self) -> str | None:
        """Return the unique ticket identifier."""
        ...

class TicketInterface(ABC):
    """The contract for ticketing service implementations."""
    @abstractmethod
    def create_ticket(
        self,
        title: str,
        description: str,
        assignee: str | None = None,
    ) -> Ticket:
        """Create a new ticket."""
        ...

    @abstractmethod
    def get_ticket(self, ticket_id: str) -> Ticket | None:
        """Return a ticket by ID, or None if not found."""
        ...

    @abstractmethod
    def search_tickets(
        self,
        query: str | None = None,
        status: TicketStatus | None = None,
    ) -> list[Ticket]:
        """Search tickets by query and/or status."""
        ...

    @abstractmethod
    def update_ticket(
        self,
        ticket_id: str,
        status: TicketStatus | None = None,
        title: str | None = None,
    ) -> Ticket:
        """Update fields on an existing ticket."""
        ...

    @abstractmethod
    def delete_ticket(self, ticket_id: str) -> bool:
        """Delete a ticket by ID."""
        ...


# -------------------------
# GLOBAL DI BINDING
# -------------------------

_client: TicketInterface | None = None


def bind_client(client: TicketInterface) -> None:
    """Bind the concrete TicketInterface implementation."""
    global _client  # noqa: PLW0603
    _client = client

_CLIENT_NOT_BOUND_ERROR = "TicketInterface client not bound"
def get_client() -> TicketInterface:
    """Return the bound TicketInterface implementation."""
    if _client is None:
        raise RuntimeError(_CLIENT_NOT_BOUND_ERROR)
    return _client
