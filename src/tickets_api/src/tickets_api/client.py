"""OSS standardized Ticketing API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime
    from uuid import UUID


class TicketStatus(StrEnum):
    """Possible lifecycle states of a ticket."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(StrEnum):
    """Priority levels for tickets."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Ticket:
    """Immutable domain model representing a ticket."""

    id: UUID
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    reporter: str
    assignee: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Comment:
    """Immutable domain model representing a ticket comment."""

    id: UUID
    ticket_id: UUID
    author: str
    content: str
    created_at: datetime


class ServiceError(Exception):
    """Base exception for ticket service errors."""


class TicketNotFoundError(ServiceError):
    """Raised when a requested ticket does not exist."""


class TicketServiceAPI(ABC):
    """Abstract interface for ticketing services."""

    @abstractmethod
    async def create_ticket(
        self,
        title: str,
        description: str,
        reporter: str,
        priority: TicketPriority = TicketPriority.MEDIUM,
        assignee: str | None = None,
    ) -> Ticket:
        """Create a new ticket."""

    @abstractmethod
    async def get_ticket(self, ticket_id: UUID) -> Ticket | None:
        """Retrieve a ticket by ID."""

    @abstractmethod
    async def list_tickets(
        self,
        status: TicketStatus | None = None,
        assignee: str | None = None,
        reporter: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Ticket]:
        """List tickets with optional filters."""

    @abstractmethod
    async def update_ticket(  # noqa: PLR0913
        self,
        ticket_id: UUID,
        title: str | None = None,
        description: str | None = None,
        status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
        assignee: str | None = None,
    ) -> Ticket | None:
        """Update mutable fields of a ticket."""

    @abstractmethod
    async def delete_ticket(self, ticket_id: UUID) -> bool:
        """Delete a ticket."""

    @abstractmethod
    async def add_comment(
        self,
        ticket_id: UUID,
        author: str,
        content: str,
    ) -> Comment | None:
        """Add a comment to a ticket."""

    @abstractmethod
    async def get_ticket_comments(self, ticket_id: UUID) -> list[Comment]:
        """Retrieve all comments for a ticket."""

    @abstractmethod
    async def transition_status(
        self,
        ticket_id: UUID,
        new_status: TicketStatus,
    ) -> Ticket | None:
        """Change the status of a ticket."""

    @abstractmethod
    async def reassign_ticket(
        self,
        ticket_id: UUID,
        new_assignee: str,
    ) -> Ticket | None:
        """Reassign a ticket to a new user."""

    @abstractmethod
    async def update_priority(
        self,
        ticket_id: UUID,
        new_priority: TicketPriority,
    ) -> Ticket | None:
        """Update the priority of a ticket."""

    @abstractmethod
    async def update_description(
        self,
        ticket_id: UUID,
        new_description: str,
    ) -> Ticket | None:
        """Update the description of a ticket."""


_get_client: Callable[[], TicketServiceAPI] | None = None


def get_client() -> TicketServiceAPI:
    """Return the registered TicketServiceAPI implementation."""
    if _get_client is None:
        msg = (
            "TicketServiceAPI client not registered. "
            "Import tickets_impl or tickets_adapter to register one."
        )
        raise RuntimeError(msg)
    return _get_client()
