from __future__ import annotations

from dataclasses import dataclass
from typing import List

from tickets_api.client import TicketStatus


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: TicketStatus
    assignee: str | None = None


# -------------------------
# IN-MEMORY STORE (FIX)
# -------------------------

_TICKETS: List[Ticket] = []


def create_ticket(title: str, description: str, assignee: str | None) -> Ticket:
    ticket = Ticket(
        id=f"TICKET-{len(_TICKETS) + 1}",
        title=title,
        description=description,
        status=TicketStatus.OPEN,
        assignee=assignee,
    )
    _TICKETS.append(ticket)
    return ticket


def list_tickets() -> list[Ticket]:
    return list(_TICKETS)
