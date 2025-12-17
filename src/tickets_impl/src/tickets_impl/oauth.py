"""OAuth helpers for Jira integration.

This module will eventually handle OAuth token acquisition
and refresh for Jira. At this stage, it contains ONLY
method skeletons.
"""

from __future__ import annotations


class JiraOAuth:
    """Skeleton OAuth helper for Jira."""

    async def get_access_token(self) -> str:
        """Return a valid Jira access token."""
        raise NotImplementedError

    async def refresh_access_token(self) -> str:
        """Refresh and return a new Jira access token."""
        raise NotImplementedError
