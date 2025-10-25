from __future__ import annotations

from abc import ABC, abstractmethod

from .types import Channel, Message, User


class ChatClient(ABC):
    """Abstract contract for Slack-like chat operations."""
    @abstractmethod
    def list_channels(self) -> list[Channel]: ...
    @abstractmethod
    def fetch_messages(self, channel_id: str, limit: int = 50) -> list[Message]: ...
    @abstractmethod
    def send_message(self, channel_id: str, text: str, thread_ts: str | None = None) -> Message: ...
    @abstractmethod
    def delete_message(self, channel_id: str, ts: str) -> bool: ...
    @abstractmethod
    def get_user(self, user_id: str) -> User: ...

def get_client() -> ChatClient:
    """Factory placeholder; will be wired to concrete impl via DI in later parts."""
    raise NotImplementedError("ChatClient factory is not wired yet.")
