from __future__ import annotations
from typing import List, Optional
import os
import httpx

# Import models / interfaces from slack_api if present.
# If names differ, Raunak will align imports in Part 4.
try:
    from slack_api.models import Channel, Message, User  # type: ignore
    from slack_api.client import ChatClient  # abstract interface
except Exception:
    # Minimal fallback dataclasses to keep code readable if import stubs fail locally.
    # Raunak will remove once exact contracts are confirmed.
    from dataclasses import dataclass

    @dataclass
    class Channel:
        id: str
        name: str

    @dataclass
    class Message:
        id: str
        channel_id: str
        text: str

    @dataclass
    class User:
        id: str
        name: str

    class ChatClient:  # noqa: N801
        async def list_channels(self, user_id: str) -> List[Channel]: ...
        async def list_messages(self, channel_id: str, limit: int = 50) -> List[Message]: ...
        async def post_message(self, channel_id: str, text: str) -> Message: ...
        async def get_user(self, user_id: str) -> Optional[User]: ...

from .token_store import TokenStore, EnvConfiguredTokenStoreImpl

SLACK_API_BASE = "https://slack.com/api"

def _bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

class SlackChatClient(ChatClient):
    """
    Concrete ChatClient implementation over Slack Web API.
    Tokens are loaded per-user via the TokenStore.
    """
    def __init__(self, token_store: Optional[TokenStore] = None) -> None:
        self.token_store: TokenStore = token_store or EnvConfiguredTokenStoreImpl()

    async def _get_token(self, user_id: str) -> str:
        bundle = self.token_store.load(user_id)
        if not bundle or not bundle.access_token:
            raise RuntimeError(
                f"No access token for user_id={user_id}. Complete OAuth first."
            )
        return bundle.access_token

    async def list_channels(self, user_id: str) -> List[Channel]:
        token = await self._get_token(user_id)
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(
                f"{SLACK_API_BASE}/conversations.list",
                headers=_bearer(token),
                params={"exclude_archived": "true", "types": "public_channel,private_channel"},
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok", False):
                raise RuntimeError(f"Slack API error: {data}")
            channels = []
            for ch in data.get("channels", []):
                channels.append(Channel(id=ch.get("id", ""), name=ch.get("name", "")))
            return channels

    async def list_messages(self, channel_id: str, limit: int = 50) -> List[Message]:
        """
        NOTE: If your abstract API requires a user context, add it and fetch token via _get_token(user_id).
        For now, use a bot/app-level token from env (fallback) to avoid changing A-signatures.
        """
        env_token = os.getenv("SLACK_BOT_TOKEN")
        if not env_token:
            raise RuntimeError("SLACK_BOT_TOKEN not set for list_messages fallback.")
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(
                f"{SLACK_API_BASE}/conversations.history",
                headers=_bearer(env_token),
                params={"channel": channel_id, "limit": str(limit)},
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok", False):
                raise RuntimeError(f"Slack API error: {data}")
            result: List[Message] = []
            for i, m in enumerate(data.get("messages", [])):
                text = m.get("text", "")
                msg_id = m.get("ts", f"{i}")
                result.append(Message(id=msg_id, channel_id=channel_id, text=text))
            return result

    async def post_message(self, channel_id: str, text: str) -> Message:
        env_token = os.getenv("SLACK_BOT_TOKEN")
        if not env_token:
            raise RuntimeError("SLACK_BOT_TOKEN not set for post_message.")
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"{SLACK_API_BASE}/chat.postMessage",
                headers=_bearer(env_token),
                data={"channel": channel_id, "text": text},
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok", False):
                raise RuntimeError(f"Slack API error: {data}")
            msg = data.get("message", {})
            msg_id = msg.get("ts", "")
            return Message(id=msg_id, channel_id=channel_id, text=msg.get("text", text))

    async def get_user(self, user_id: str) -> Optional[User]:
        env_token = os.getenv("SLACK_BOT_TOKEN")
        if not env_token:
            raise RuntimeError("SLACK_BOT_TOKEN not set for get_user.")
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(
                f"{SLACK_API_BASE}/users.info",
                headers=_bearer(env_token),
                params={"user": user_id},
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok", False):
                return None
            u = data.get("user", {}) or {}
            return User(id=u.get("id", user_id), name=u.get("name", "unknown"))
