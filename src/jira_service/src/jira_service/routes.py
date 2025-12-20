from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel

from jira_service.models import (
    TicketStatus,
    create_ticket,
    list_tickets,
)

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
