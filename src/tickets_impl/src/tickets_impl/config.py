"""Jira-backed TicketServiceAPI registration."""

from tickets_api.client import register_client
from tickets_impl.impl import TicketImpl


def _register() -> None:
    register_client(TicketImpl)


_register()
