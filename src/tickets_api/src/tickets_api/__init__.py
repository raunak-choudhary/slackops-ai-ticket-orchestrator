"""Tickets API.

Defines the OSS-standardized abstract interfaces for ticketing services.

This package is provider-agnostic and must not import any implementation code.
"""

from __future__ import annotations

from tickets_api.client import (
    Ticket,
    TicketInterface,
    TicketStatus,
    get_client,
)

__all__ = [
    "Ticket",
    "TicketInterface",
    "TicketStatus",
    "get_client",
]
