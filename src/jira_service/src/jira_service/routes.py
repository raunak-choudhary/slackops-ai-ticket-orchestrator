"""HTTP routes for the Jira ticket service.

Routes delegate to the OSS ticket client retrieved via tickets_api.get_client(),
which is injected by importing jira_impl.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from tickets_api import client as tickets_api_client
from tickets_api.client import TicketStatus

# Importing jira_impl activates dependency injection:
# it monkey-patches tickets_api_client.get_client().
import jira_impl  # noqa: F401

from jira_service.models import (
    HealthResponse,
    TicketIn,
    TicketOut,
    TicketUpdateIn,
    TicketsResponse,
)

router = APIRouter()


def _to_ticket_out(ticket: object) -> TicketOut:
    """Convert a tickets_api Ticket to a TicketOut model."""
    # Ticket is an ABC with properties; we access attributes by contract.
    return TicketOut(
        id=getattr(ticket, "id"),
        title=getattr(ticket, "title"),
        description=getattr(ticket, "description"),
        status=getattr(ticket, "status"),
        assignee=getattr(ticket, "assignee"),
    )


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Simple liveness probe."""
    return HealthResponse(status="ok")


@router.post("/tickets", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketIn) -> TicketOut:
    """Create a new ticket."""
    try:
        client = tickets_api_client.get_client()
        ticket = client.create_ticket(
            title=payload.title,
            description=payload.description,
            assignee=payload.assignee,
        )
        return _to_ticket_out(ticket)
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Jira is unreachable") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str) -> TicketOut:
    """Get a ticket by its ID."""
    try:
        client = tickets_api_client.get_client()
        ticket = client.get_ticket(ticket_id)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return _to_ticket_out(ticket)
    except HTTPException:
        raise
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Jira is unreachable") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/tickets", response_model=TicketsResponse)
def search_tickets(
    query: str | None = Query(default=None),
    status_filter: TicketStatus | None = Query(default=None, alias="status"),
) -> TicketsResponse:
    """Search tickets by query and/or status."""
    try:
        client = tickets_api_client.get_client()
        tickets = client.search_tickets(query=query, status=status_filter)
        return TicketsResponse(tickets=[_to_ticket_out(t) for t in tickets])
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Jira is unreachable") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.put("/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: str, payload: TicketUpdateIn) -> TicketOut:
    """Update a ticket (OSS-compatible).

    Note: Jira status transitions are workflow-specific; the Jira impl currently
    accepts status but may not perform a workflow transition.
    """
    try:
        client = tickets_api_client.get_client()
        updated = client.update_ticket(
            ticket_id=ticket_id,
            status=payload.status,
            title=payload.title,
        )
        return _to_ticket_out(updated)
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Jira is unreachable") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Ticket not found") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.delete("/tickets/{ticket_id}", response_model=dict[str, bool])
def delete_ticket(ticket_id: str) -> dict[str, bool]:
    """Delete a ticket."""
    try:
        client = tickets_api_client.get_client()
        ok = client.delete_ticket(ticket_id)
        return {"deleted": ok}
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Jira is unreachable") from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal server error") from exc
