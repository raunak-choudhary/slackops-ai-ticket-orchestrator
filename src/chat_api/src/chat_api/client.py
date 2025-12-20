"""Abstract interfaces for Chat APIs."""

from abc import ABC, abstractmethod


class Message(ABC):
    """Abstract representation of a chat message.

    Implementations should wrap platform-specific message objects
    (e.g., Slack, Discord, Teams) behind this common interface.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the message."""
        raise NotImplementedError

    @property
    @abstractmethod
    def content(self) -> str:
        """The actual text content of the message."""
        raise NotImplementedError

    @property
    @abstractmethod
    def sender_id(self) -> str:
        """The ID of the user who sent the message."""
        raise NotImplementedError


class ChatInterface(ABC):
    """A minimal interface for sending and receiving messages."""

    @abstractmethod
    def send_message(self, channel_id: str, content: str) -> bool:
        """Send a message to a specific destination (channel/thread)."""
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]:
        """Read the last N messages from a destination."""
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, channel_id: str, message_id: str) -> bool:
        """Delete a specific message. Returns True if successful."""
        raise NotImplementedError


def get_client() -> ChatInterface:
    """Return an instance of a Chat Client.

    This function should be replaced by implementation packages.
    Import an implementation package (e.g., slack_impl) to inject
    the concrete implementation.

    Returns:
        ChatInterface instance from the injected implementation

    Raises:
        NotImplementedError: If no implementation has been imported
    """
    raise NotImplementedError
