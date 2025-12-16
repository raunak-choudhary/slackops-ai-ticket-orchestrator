"""HTTP routes for the Slack Service.

This module defines all FastAPI endpoints exposed by the Slack service.
It acts purely as a server-side adapter that translates HTTP requests
into calls against the abstract chat API interface.

Key architectural principles:
- This service does NOT know about Slack internals.
- All provider logic is accessed via `chat_api.get_client()`.
- The Slack implementation is injected via import side effects.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Path

import chat_api
import slack_impl  # noqa: F401  # Triggers dependency injection

from slack_service.models import (
    HealthResponse,
    MessageOut,
    MessagesResponse,
    PostMessageIn,
    PostMessageResponse,
    MembersResponse,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint for the Slack service.

    This endpoint is used by deployment systems and tests to verify
    that the service process is running and responsive.

    Returns:
        HealthResponse indicating service health.
    """
    return HealthResponse(ok=True)


@router.get(
    "/channels/{channel_id}/messages",
    response_model=MessagesResponse,
)
def list_channel_messages(
    channel_id: Annotated[str, Path(min_length=1)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> MessagesResponse:
    """Retrieve messages from a channel.

    This endpoint fetches messages using the abstract chat interface.
    The underlying provider implementation is injected via
    `slack_impl` at import time.

    Args:
        channel_id: Identifier of the channel to read messages from.
        limit: Maximum number of messages to return (1–100).

    Returns:
        MessagesResponse containing the list of messages.

    Raises:
        HTTPException: If message retrieval fails.
    """
    try:
        client = chat_api.get_client()
        messages = client.get_messages(channel_id=channel_id, limit=limit)

        return MessagesResponse(
            messages=[
                MessageOut(
                    id=msg.id,
                    channel_id=channel_id,
                    text=msg.content,
                    sender_id=msg.sender_id,
                    ts=msg.id,
                )
                for msg in messages
            ]
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve messages: {exc!s}",
        ) from exc


@router.post(
    "/channels/{channel_id}/messages",
    response_model=PostMessageResponse,
)
def post_channel_message(
    channel_id: Annotated[str, Path(min_length=1)],
    payload: PostMessageIn,
) -> PostMessageResponse:
    """Post a message to a channel.

    This endpoint sends a message using the abstract chat interface.
    The service does not know or care which provider is used.

    Args:
        channel_id: Identifier of the channel.
        payload: Message content payload.

    Returns:
        PostMessageResponse containing the posted message.

    Raises:
        HTTPException: If sending the message fails.
    """
    try:
        client = chat_api.get_client()
        success = client.send_message(
            channel_id=channel_id,
            content=payload.text,
        )

        if not success:
            raise RuntimeError("Message send operation returned False")

        return PostMessageResponse(
            message=MessageOut(
                id="unknown",
                channel_id=channel_id,
                text=payload.text,
                sender_id=None,
                ts=None,
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message: {exc!s}",
        ) from exc


@router.delete(
    "/channels/{channel_id}/messages/{message_id}",
)
def delete_channel_message(
    channel_id: Annotated[str, Path(min_length=1)],
    message_id: Annotated[str, Path(min_length=1)],
) -> dict[str, str]:
    """Delete a message from a channel.

    This endpoint deletes a message via the abstract chat interface.

    Args:
        channel_id: Identifier of the channel.
        message_id: Identifier of the message to delete.

    Returns:
        A confirmation dictionary.

    Raises:
        HTTPException: If deletion fails.
    """
    try:
        client = chat_api.get_client()
        client.delete_message(
            channel_id=channel_id,
            message_id=message_id,
        )

        return {"status": "deleted"}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete message: {exc!s}",
        ) from exc


@router.get(
    "/channels/{channel_id}/members",
    response_model=MembersResponse,
)
def list_channel_members(
    channel_id: Annotated[str, Path(min_length=1)],
) -> MembersResponse:
    """List members of a channel.

    NOTE:
    This endpoint assumes that the injected chat client provides
    a provider-specific extension for retrieving channel members.
    If unavailable, this method should be implemented in `slack_impl`
    and exposed via the injected client.

    Args:
        channel_id: Identifier of the channel.

    Returns:
        MembersResponse containing member identifiers.

    Raises:
        HTTPException: If member listing fails.
    """
    try:
        client = chat_api.get_client()

        # This is intentionally a soft dependency on provider extensions.
        # If not implemented yet, slack_impl should be updated later.
        members = getattr(client, "get_channel_members")(channel_id)

        return MembersResponse(members=list(members))

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list channel members: {exc!s}",
        ) from exc
