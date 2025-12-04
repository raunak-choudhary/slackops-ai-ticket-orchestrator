from typing import List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from chat_api.client import ChatClient
from chat_api.types import Channel, ChatMessage


class SlackChatClient(ChatClient):
    """
    Slack implementation of the shared ChatClient interface.
    """

    def __init__(self, token: str) -> None:
        self.client = WebClient(token=token)

    # ----------------------------------------------------
    # Channels
    # ----------------------------------------------------

    def get_channels(self) -> List[Channel]:
        try:
            resp = self.client.conversations_list()
            return [
                Channel(
                    id=c["id"],
                    name=c.get("name", ""),
                    metadata=c,
                )
                for c in resp.get("channels", [])
            ]
        except SlackApiError as e:
            raise RuntimeError(f"Slack error getting channels: {e}") from e

    def get_channel(self, channel_id: str) -> Channel:
        try:
            resp = self.client.conversations_info(channel=channel_id)
            c = resp["channel"]
            return Channel(id=c["id"], name=c.get("name", ""), metadata=c)
        except SlackApiError as e:
            raise RuntimeError(f"Slack error getting channel: {e}") from e

    # ----------------------------------------------------
    # Messages
    # ----------------------------------------------------

    def send_message(self, channel_id: str, content: str) -> ChatMessage:
        try:
            resp = self.client.chat_postMessage(channel=channel_id, text=content)
            return ChatMessage(
                id=resp["ts"],
                channel_id=channel_id,
                text=content,
                metadata=resp,
            )
        except SlackApiError as e:
            raise RuntimeError(f"Slack error sending message: {e}") from e

    def get_messages(self, channel_id: str, limit: int = 50) -> List[ChatMessage]:
        try:
            resp = self.client.conversations_history(channel=channel_id, limit=limit)
            return [
                ChatMessage(
                    id=m["ts"],
                    channel_id=channel_id,
                    text=m.get("text", ""),
                    metadata=m,
                )
                for m in resp.get("messages", [])
            ]
        except SlackApiError as e:
            raise RuntimeError(f"Slack error getting messages: {e}") from e

    def get_message(self, channel_id: str, message_id: str) -> ChatMessage:
        """
        Slack has no fetch-by-id API.
        Cheapest workaround: fetch recent messages and search.
        """
        msgs = self.get_messages(channel_id, limit=100)

        for msg in msgs:
            if msg.id == message_id:
                return msg

        raise RuntimeError(f"Message {message_id} not found in channel {channel_id}")

    def delete_message(self, channel_id: str, message_id: str) -> None:
        """
        Slack requires both channel_id AND ts to delete a message.
        """
        try:
            self.client.chat_delete(channel=channel_id, ts=message_id)
        except SlackApiError:
            # per Chat API agreement → soft fail
            return
