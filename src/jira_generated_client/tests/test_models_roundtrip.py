"""Basic model serialization round-trip tests."""

from tickets_service_api_client.models.ticket_in import TicketIn
from tickets_service_api_client.models.ticket_out import TicketOut


def test_ticket_in_roundtrip() -> None:
    """TicketIn should serialize and deserialize correctly."""
    ticket = TicketIn(title="Test title", description="Test description")
    data = ticket.to_dict()
    restored = TicketIn.from_dict(data)

    assert restored.title == "Test title"
    assert restored.description == "Test description"


def test_ticket_out_roundtrip() -> None:
    """TicketOut should serialize and deserialize correctly."""
    ticket = TicketOut(
        id="PROJ-1",
        title="Bug",
        description="Something broke",
        status="open",
    )
    data = ticket.to_dict()
    restored = TicketOut.from_dict(data)

    assert restored.id == "PROJ-1"
    assert restored.status == "open"
