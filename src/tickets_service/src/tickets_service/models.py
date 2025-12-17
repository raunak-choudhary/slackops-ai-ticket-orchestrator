"""Pydantic models for Tickets Service."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    ok: bool


class TicketIn(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None


class TicketOut(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: str


class TicketsResponse(BaseModel):
    tickets: list[TicketOut]
