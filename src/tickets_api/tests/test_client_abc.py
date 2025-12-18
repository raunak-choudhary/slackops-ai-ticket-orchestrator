"""Abstract base class tests for TicketInterface."""

from __future__ import annotations

import inspect

from tickets_api.client import TicketInterface


def test_ticket_interface_is_abstract() -> None:
    """TicketInterface must be an abstract base class."""
    assert inspect.isabstract(TicketInterface)
