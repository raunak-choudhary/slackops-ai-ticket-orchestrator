"""Public API symbol tests for tickets_api."""

from tickets_api.client import (
    Ticket,
    TicketInterface,
    TicketStatus,
    get_client,
)


def test_public_symbols_exist() -> None:
    """Ensure expected public symbols are exposed."""
    assert Ticket is not None
    assert TicketInterface is not None
    assert TicketStatus is not None
    assert get_client is not None
