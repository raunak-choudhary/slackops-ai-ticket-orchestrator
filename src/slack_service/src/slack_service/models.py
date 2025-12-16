"""Pydantic models for the Slack Service HTTP adapter.

This module defines request and response schemas used by the FastAPI routes.
Models here are intentionally provider-agnostic and represent the HTTP surface
area of the service.

Notes:
- The underlying chat provider is accessed via `chat_api.get_client()` using
  dependency injection.
- These models avoid Slack-specific SDK types and keep the service layer clean.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response payload for the health check endpoint.

    Attributes:
        ok: Indicates whether the service is healthy.
    """

    ok: bool


class ChannelOut(BaseModel):
    """Public representation of a chat channel.

    Attributes:
        id: Unique identifier for the channel.
        name: Human-readable channel name.
    """

    id: str = Field(..., description="Channel identifier")
    name: str = Field(..., description="Human-readable channel name")


class MessageOut(BaseModel):
    """Public representation of a message returned by the service.

    Attributes:
        id: Unique message identifier (provider-defined).
        channel_id: Channel identifier where the message belongs.
        text: Message content as plain text.
        sender_id: Identifier of the sender when known.
        ts: Optional timestamp-like string for UI compatibility. If the backing
            provider does not supply one, the service may synthesize it.
    """

    id: str = Field(..., description="Message identifier")
    channel_id: str = Field(..., description="Channel identifier")
    text: str = Field(..., description="Message content")
    sender_id: str | None = Field(default=None, description="Sender identifier")
    ts: str | None = Field(default=None, description="Timestamp-like string")


class MessagesResponse(BaseModel):
    """Wrapper response used when listing channel messages.

    Attributes:
        messages: List of messages in the channel.
    """

    messages: list[MessageOut]


class PostMessageIn(BaseModel):
    """Request payload for posting a message to a channel.

    Attributes:
        text: Message content to send.
    """

    text: str = Field(..., min_length=1, description="Message content to send")


class PostMessageWithChannelIn(PostMessageIn):
    """Request payload used by a convenience endpoint that includes channel_id.

    Attributes:
        channel_id: Channel identifier where the message should be posted.
        text: Message content to send.
    """

    channel_id: str = Field(..., min_length=1, description="Channel identifier")


class PostMessageResponse(BaseModel):
    """Response payload for posting a message to a channel.

    Attributes:
        message: The posted message as returned by the service.
    """

    message: MessageOut


class MembersResponse(BaseModel):
    """Response payload for listing members of a channel.

    Attributes:
        members: List of member identifiers.
    """

    members: list[str]
