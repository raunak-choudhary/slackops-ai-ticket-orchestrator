"""Abstract interfaces for Ticketing APIs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import StrEnum


class TicketStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class Ticket(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def title(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @property
    @abstractmethod
    def status(self) -> TicketStatus: ...

    @property
    @abstractmethod
    def assignee(self) -> str | None: ...


class TicketInterface(ABC):
    @abstractmethod
    def create_ticket(
        self,
        title: str,
        description: str,
        assignee: str | None = None,
    ) -> Ticket: ...

    @abstractmethod
    def get_ticket(self, ticket_id: str) -> Ticket | None: ...

    @abstractmethod
    def search_tickets(
        self,
        query: str | None = None,
        status: TicketStatus | None = None,
    ) -> list[Ticket]: ...

    @abstractmethod
    def update_ticket(
        self,
        ticket_id: str,
        status: TicketStatus | None = None,
        title: str | None = None,
    ) -> Ticket: ...

    @abstractmethod
    def delete_ticket(self, ticket_id: str) -> bool: ...


# -------------------------
# GLOBAL DI BINDING
# -------------------------

_client: TicketInterface | None = None


def bind_client(client: TicketInterface) -> None:
    global _client
    _client = client


def get_client() -> TicketInterface:
    if _client is None:
        raise RuntimeError("TicketInterface client not bound")
    return _client
