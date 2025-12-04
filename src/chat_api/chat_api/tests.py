from dataclasses import dataclass
from typing import Optional


@dataclass
class Channel:
    id: str
    name: str
    topic: Optional[str] = None
    is_private: bool = False


@dataclass
class ChatMessage:
    id: str
    channel_id: str
    sender: str
    content: str
    ts: Optional[str] = None
