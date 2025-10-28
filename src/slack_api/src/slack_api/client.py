from __future__ import annotations

from typing import Iterable, Protocol

from .types import Channel, Message


class ChatClient(Protocol):
    """Protocol for a Slack-like chat client.

    Concrete implementations (e.g., slack_impl.SlackClient, adapters) should
    satisfy this interface. Using a Protocol keeps us decoupled from any base
    classes and friendly to static typing.
    """

    def health(self) -> bool:  # pragma: no cover - exercised via fakes/adapters
        """Return True if the underlying service is healthy."""
        ...

    def list_channels(self) -> Iterable[Channel]:
        """List accessible channels."""
        ...

    def post_message(self, channel_id: str, text: str) -> Message:
        """Post a message to a channel and return the created message."""
        ...