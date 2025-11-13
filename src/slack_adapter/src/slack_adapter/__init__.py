"""Public API surface for the slack_adapter package."""

from __future__ import annotations

from .adapter import (
    Channel,
    Message,
    ServiceAdapter,
    ServiceBackedClient,
    SlackServiceBackedClient,
)

# Explicit public API (sorted for Ruff RUF022)
__all__ = [
    "Channel",
    "Message",
    "ServiceAdapter",
    "ServiceBackedClient",
    "SlackServiceBackedClient",
]

