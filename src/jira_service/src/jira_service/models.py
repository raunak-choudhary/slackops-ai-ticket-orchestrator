"""Pydantic models for Jira ticket HTTP requests/responses."""

from __future__ import annotations

from pydantic import BaseModel, Field

from tickets_api.client import TicketStatus


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., examples=["ok"])


class TicketIn(BaseModel):
    """Create ticket request model."""

    title: str = Field(..., min_length=1, examples=["Bug: login fails"])
    description: str = Field(..., min_length=1, examples=["Steps to reproduce..."])
    assignee: str | None = Field(default=None, examples=["acct_12345"])


class TicketUpdateIn(BaseModel):
    """Update ticket request model (OSS-compatible)."""

    status: TicketStatus | None = Field(default=None)
    title: str | None = Field(default=None, min_length=1)


class TicketOut(BaseModel):
    """Ticket response model."""

    id: str
    title: str
    description: str
    status: TicketStatus
    assignee: str | None = None


class TicketsResponse(BaseModel):
    """List/search tickets response model."""

    tickets: list[TicketOut]
