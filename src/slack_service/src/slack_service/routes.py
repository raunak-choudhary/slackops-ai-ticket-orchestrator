"""HTTP routes for the Slack Service.

This module defines all FastAPI endpoints exposed by the Slack service.
"""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Path, status

import chat_api
import slack_impl  # noqa: F401  # Triggers dependency injection for ChatInterface
from slack_impl.slack_client import SlackClient

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
    """Health check endpoint for the Slack service."""
    return HealthResponse(ok=True)


@router.get(
    "/channels/{channel_id}/messages",
    response_model=MessagesResponse,
)
def list_channel_messages(
    channel_id: Annotated[str, Path(min_length=1)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> MessagesResponse:
    """Retrieve messages from a channel using the abstract chat interface."""
    print("SLACK SERVICE: list_channel_messages channel_id=", channel_id, "limit=", limit)

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

    except RuntimeError as exc:
        print("SLACK SERVICE ERROR: list_channel_messages RuntimeError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Slack authentication failed while retrieving messages",
        )

    except ConnectionError as exc:
        print("SLACK SERVICE ERROR: list_channel_messages ConnectionError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Slack while retrieving messages",
        )


@router.post(
    "/channels/{channel_id}/messages",
    response_model=PostMessageResponse,
)
def post_channel_message(
    channel_id: Annotated[str, Path(min_length=1)],
    payload: PostMessageIn,
) -> PostMessageResponse:
    """Post a message to a channel using the abstract chat interface."""
    print("SLACK SERVICE: post_channel_message channel_id=", channel_id)

    try:
        client = chat_api.get_client()
        success = client.send_message(
            channel_id=channel_id,
            content=payload.text,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Slack did not confirm message delivery",
            )

        return PostMessageResponse(
            message=MessageOut(
                id="unknown",
                channel_id=channel_id,
                text=payload.text,
                sender_id=None,
                ts=None,
            )
        )

    except RuntimeError as exc:
        print("SLACK SERVICE ERROR: post_channel_message RuntimeError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Slack authentication failed while sending message",
        )

    except ConnectionError as exc:
        print("SLACK SERVICE ERROR: post_channel_message ConnectionError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Slack while sending message",
        )


@router.delete(
    "/channels/{channel_id}/messages/{message_id}",
)
def delete_channel_message(
    channel_id: Annotated[str, Path(min_length=1)],
    message_id: Annotated[str, Path(min_length=1)],
) -> dict[str, str]:
    """Delete a message from a channel using the abstract chat interface."""
    print("SLACK SERVICE: delete_channel_message channel_id=", channel_id, "message_id=", message_id)

    try:
        client = chat_api.get_client()
        client.delete_message(
            channel_id=channel_id,
            message_id=message_id,
        )

        return {"status": "deleted"}

    except RuntimeError as exc:
        print("SLACK SERVICE ERROR: delete_channel_message RuntimeError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Slack authentication failed while deleting message",
        )

    except ConnectionError as exc:
        print("SLACK SERVICE ERROR: delete_channel_message ConnectionError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Slack while deleting message",
        )


@router.get(
    "/channels/{channel_id}/members",
    response_model=MembersResponse,
)
def list_channel_members(
    channel_id: Annotated[str, Path(min_length=1)],
) -> MembersResponse:
    """List members of a channel using the Slack provider implementation."""
    print("SLACK SERVICE: list_channel_members channel_id=", channel_id)

    try:
        base_url = os.environ["SLACK_API_BASE_URL"]
        token = os.environ["SLACK_BOT_TOKEN"]

        slack_client = SlackClient(base_url=base_url, token=token)
        members = slack_client.get_channel_members(channel_id)

        return MembersResponse(members=list(members))

    except KeyError as exc:
        print("SLACK SERVICE ERROR: list_channel_members missing env:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing required Slack environment variable: {exc}",
        )

    except RuntimeError as exc:
        print("SLACK SERVICE ERROR: list_channel_members RuntimeError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Slack authentication failed while listing channel members",
        )

    except ConnectionError as exc:
        print("SLACK SERVICE ERROR: list_channel_members ConnectionError:", repr(exc))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Slack while listing channel members",
        )
