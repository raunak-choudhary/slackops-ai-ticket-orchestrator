"""HTTP routes for the Tickets Service."""

from fastapi import APIRouter, HTTPException, Path

from tickets_service.models import (
    HealthResponse,
    TicketIn,
    TicketOut,
    TicketsResponse,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(ok=True)


@router.get("/tickets", response_model=TicketsResponse)
def list_tickets() -> TicketsResponse:
    try:
        import tickets_api  # runtime import (DI activation)

        client = tickets_api.get_client()
        tickets = client.list_tickets()

        return TicketsResponse(
            tickets=[
                TicketOut(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    status=t.status,
                )
                for t in tickets
            ]
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list tickets: {exc}",
        ) from exc


@router.post("/tickets", response_model=TicketOut)
def create_ticket(ticket: TicketIn) -> TicketOut:
    try:
        import tickets_api  # runtime import (DI activation)

        client = tickets_api.get_client()
        created = client.create_ticket(
            title=ticket.title,
            description=ticket.description,
        )

        return TicketOut(
            id=created.id,
            title=created.title,
            description=created.description,
            status=created.status,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create ticket: {exc}",
        ) from exc


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: str = Path(..., min_length=1),
) -> TicketOut:
    try:
        import tickets_api  # runtime import (DI activation)

        client = tickets_api.get_client()
        ticket = client.get_ticket(ticket_id)

        return TicketOut(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch ticket: {exc}",
        ) from exc
