from __future__ import annotations

from fastapi import APIRouter, status

from jira_service.models import create_ticket, list_tickets, Ticket
from jira_service.models import TicketStatus
from jira_service.models import Ticket as TicketModel
from jira_service.models import TicketStatus as StatusEnum

from jira_service.models import Ticket as InternalTicket
from jira_service.models import TicketStatus
from jira_service.models import create_ticket as create_ticket_internal
from jira_service.models import list_tickets as list_tickets_internal

from jira_service.models import Ticket as StoredTicket
from jira_service.models import TicketStatus
from jira_service.models import create_ticket
from jira_service.models import list_tickets

from pydantic import BaseModel


router = APIRouter()


class TicketIn(BaseModel):
    title: str
    description: str
    assignee: str | None = None


class TicketOut(BaseModel):
    id: str
    title: str
    description: str
    status: TicketStatus
    assignee: str | None


class TicketsResponse(BaseModel):
    tickets: list[TicketOut]


@router.post("/tickets", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket_route(payload: TicketIn) -> TicketOut:
    ticket = create_ticket(
        title=payload.title,
        description=payload.description,
        assignee=payload.assignee,
    )
    return TicketOut(**ticket.__dict__)


@router.get("/tickets", response_model=TicketsResponse)
def list_tickets_route() -> TicketsResponse:
    tickets = list_tickets()
    return TicketsResponse(
        tickets=[TicketOut(**t.__dict__) for t in tickets]
    )
