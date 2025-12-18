"""
Service-backed Slack adapter.

Implements chat_api.ChatInterface by delegating all operations
to the Slack FastAPI service via the auto-generated HTTP client.
"""

from __future__ import annotations

import os

from chat_api import ChatInterface, Message

from slack_service_api_client import Client
from slack_service_api_client.api.default import (
    delete_channel_message_channels_channel_id_messages_message_id_delete,
    list_channel_members_channels_channel_id_members_get,
    list_channel_messages_channels_channel_id_messages_get,
    post_channel_message_channels_channel_id_messages_post,
)
from slack_service_api_client.models.post_message_in import PostMessageIn
from slack_service_api_client.models.members_response import MembersResponse


# -------------------------
# Domain Message Wrapper
# -------------------------

class SlackServiceMessage(Message):
    """Concrete Message implementation backed by slack_service responses."""

    def __init__(self, id: str, content: str, sender_id: str) -> None:
        self._id = id
        self._content = content
        self._sender_id = sender_id

    @property
    def id(self) -> str:
        return self._id

    @property
    def content(self) -> str:
        return self._content

    @property
    def sender_id(self) -> str:
        return self._sender_id


# -------------------------
# Adapter Implementation
# -------------------------

class SlackServiceClient(ChatInterface):
    """ChatInterface implementation backed by slack_service over HTTP."""

    def __init__(self) -> None:
        base_url = os.environ["SLACK_SERVICE_BASE_URL"]
        self._client = Client(base_url=base_url)

    def send_message(self, channel_id: str, content: str) -> bool:
        try:
            response = post_channel_message_channels_channel_id_messages_post.sync(
                client=self._client,
                channel_id=channel_id,
                body=PostMessageIn(text=content),
            )
            return response is not None
        except Exception as exc:
            raise ConnectionError("Failed to send message") from exc

    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]:
        try:
            response = list_channel_messages_channels_channel_id_messages_get.sync(
                client=self._client,
                channel_id=channel_id,
                limit=limit,
            )

            if response is None or not hasattr(response, "messages"):
                return []

            return [
                SlackServiceMessage(
                    id=msg.id,
                    content=msg.text,
                    sender_id=msg.sender_id or "",
                )
                for msg in response.messages
            ]

        except Exception as exc:
            raise ConnectionError("Failed to fetch messages") from exc

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        try:
            response = (
                delete_channel_message_channels_channel_id_messages_message_id_delete.sync(
                    client=self._client,
                    channel_id=channel_id,
                    message_id=message_id,
                )
            )
            return response is not None
        except Exception as exc:
            raise ConnectionError("Failed to delete message") from exc

    # Slack-specific extension
    def get_channel_members(self, channel_id: str) -> list[str]:
        try:
            response = list_channel_members_channels_channel_id_members_get.sync(
                client=self._client,
                channel_id=channel_id,
            )

            if not isinstance(response, MembersResponse):
                return []

            return list(response.members)

        except Exception as exc:
            raise ConnectionError("Failed to list members") from exc
