"""Tests for Slack service Pydantic models."""

import pytest
from pydantic import ValidationError

from slack_service.models import (
    MessageOut,
    MessagesResponse,
    PostMessageIn,
    PostMessageResponse,
    MembersResponse,
)


def test_message_out_creation() -> None:
    """MessageOut model should be created correctly."""
    msg = MessageOut(
        id="m1",
        channel_id="c1",
        text="hello",
        sender_id="u1",
        ts="123",
    )

    assert msg.id == "m1"
    assert msg.text == "hello"


def test_post_message_in_requires_text() -> None:
    """PostMessageIn should require text."""
    with pytest.raises(ValidationError):
        PostMessageIn()  # type: ignore[call-arg]


def test_messages_response_wraps_list() -> None:
    """MessagesResponse wraps message list."""
    resp = MessagesResponse(messages=[])

    assert resp.messages == []


def test_post_message_response_structure() -> None:
    """PostMessageResponse wraps MessageOut."""
    msg = MessageOut(
        id="m1",
        channel_id="c1",
        text="hello",
        sender_id=None,
        ts=None,
    )

    resp = PostMessageResponse(message=msg)

    assert resp.message.id == "m1"


def test_members_response_accepts_list() -> None:
    """MembersResponse accepts member list."""
    resp = MembersResponse(members=["u1", "u2"])

    assert resp.members == ["u1", "u2"]
