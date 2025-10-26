from __future__ import annotations
from typing import List, Optional

# Contract imports
try:
    from slack_api.models import Channel, Message, User  # type: ignore
    from slack_api.client import ChatClient  # abstract interface
except Exception:
    # Same minimal fallback as before; Raunak will align.
    from dataclasses import dataclass
    @dataclass
    class Channel: id: str; name: str
    @dataclass
    class Message: id: str; channel_id: str; text: str
    @dataclass
    class User: id: str; name: str
    class ChatClient:  # noqa: N801
        async def list_channels(self, user_id: str) -> List[Channel]: ...
        async def list_messages(self, channel_id: str, limit: int = 50) -> List[Message]: ...
        async def post_message(self, channel_id: str, text: str) -> Message: ...
        async def get_user(self, user_id: str) -> Optional[User]: ...

# TODO: Raunak will generate this client from /openapi.json and replace the import below.
# from generated_clients.slack_service_client import SlackServiceClient

class NetworkBackedSlackClient(ChatClient):
    """
    Adapter that implements the abstract API by delegating to the type-safe
    client generated from the service's OpenAPI schema.
    """
    def __init__(self, base_url: str, auth: Optional[str] = None) -> None:
        self.base_url = base_url
        self.auth = auth
        # self.client = SlackServiceClient(base_url=base_url, auth=auth)  # TODO wire in Part 4

    async def list_channels(self, user_id: str) -> List[Channel]:
        # resp = await self.client.channels_list(user_id=user_id)
        # return [Channel(id=c.id, name=c.name) for c in resp.data]
        raise NotImplementedError("Wire to generated client in Part 4 (Raunak).")

    async def list_messages(self, channel_id: str, limit: int = 50) -> List[Message]:
        # resp = await self.client.messages_list(channel_id=channel_id, limit=limit)
        # return [Message(id=m.id, channel_id=m.channel_id, text=m.text) for m in resp.data]
        raise NotImplementedError("Wire to generated client in Part 4 (Raunak).")

    async def post_message(self, channel_id: str, text: str) -> Message:
        # msg = await self.client.messages_post(channel_id=channel_id, text=text)
        # return Message(id=msg.id, channel_id=msg.channel_id, text=msg.text)
        raise NotImplementedError("Wire to generated client in Part 4 (Raunak).")

    async def get_user(self, user_id: str) -> Optional[User]:
        # u = await self.client.users_get(user_id=user_id)
        # return User(id=u.id, name=u.name) if u else None
        raise NotImplementedError("Wire to generated client in Part 4 (Raunak).")
