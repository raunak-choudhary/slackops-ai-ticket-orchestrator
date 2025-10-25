from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Channel:
    id: str
    name: str

@dataclass(slots=True, frozen=True)
class Message:
    channel_id: str
    ts: str          # Slack timestamp identifier
    text: str
    user_id: str | None = None
    thread_ts: str | None = None

@dataclass(slots=True, frozen=True)
class User:
    id: str
    name: str
    real_name: str | None = None
