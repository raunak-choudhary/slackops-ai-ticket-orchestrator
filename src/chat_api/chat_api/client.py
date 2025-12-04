from abc import ABC, abstractmethod
from typing import Iterator, List
from .types import Channel, ChatMessage


class ChatClient(ABC):
    """
    Standard interface shared by all Chat teams.
    """

    @abstractmethod
    def get_channels(self) -> List[Channel]:
        """Return all channels."""
        raise NotImplementedError

    @abstractmethod
    def get_channel(self, channel_id: str) -> Channel:
        """Return a single channel by id."""
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, channel_id: str, limit: int = 50) -> List[ChatMessage]:
        """Return recent messages from the specified channel."""
        raise NotImplementedError

    @abstractmethod
    def get_message(self, message_id: str) -> ChatMessage | None:
        """Return a single message by id."""
        raise NotImplementedError

    @abstractmethod
    def send_message(self, channel_id: str, content: str) -> ChatMessage:
        """Send a message to a channel and return the sent message."""
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, message_id: str) -> None:
        """Delete a message by id."""
        raise NotImplementedError
