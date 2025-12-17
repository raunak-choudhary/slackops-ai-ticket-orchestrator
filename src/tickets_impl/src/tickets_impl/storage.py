"""Storage helpers for tickets_impl.

This module will eventually persist Jira tokens and
ticket-related metadata. At this stage, it contains
ONLY method skeletons.
"""

from __future__ import annotations


class TicketStorage:
    """Skeleton storage abstraction for tickets."""

    async def save_ticket(self, *args, **kwargs):
        raise NotImplementedError

    async def get_ticket(self, *args, **kwargs):
        raise NotImplementedError

    async def delete_ticket(self, *args, **kwargs):
        raise NotImplementedError

    async def save_token(self, *args, **kwargs):
        raise NotImplementedError

    async def get_token(self, *args, **kwargs):
        raise NotImplementedError
