"""Jira-backed implementation of the TicketServiceAPI.

Importing this module registers the tickets_impl implementation
with the tickets_api dependency injection hook.
"""

import tickets_api.client as tickets_client

from tickets_impl.impl import TicketImpl


def _register() -> None:
    """Register TicketImpl as the active TicketServiceAPI implementation."""
    tickets_client._get_client = TicketImpl  # type: ignore[attr-defined]


_register()

__all__ = ["TicketImpl"]
