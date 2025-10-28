from __future__ import annotations

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from slack_api import Channel, Message  # for type hints only

# Concrete client from impl and types from API contract
from slack_impl.slack_client import SlackClient

app = FastAPI(
    title="Slack Chat Service (HW2)",
    version="0.1.0",
    description="FastAPI wrapper around slack_impl.SlackClient",
)


def get_client() -> SlackClient:
    # DI factory – easy to override in tests if needed
    return SlackClient()


@app.get("/health")
def health(client: SlackClient = Depends(get_client)) -> dict[str, bool]:
    ok = bool(client.health())
    return {"ok": ok}


@app.get("/channels")
def list_channels(client: SlackClient = Depends(get_client)) -> list[dict[str, str]]:
    channels: list[Channel] = client.list_channels()
    # Return plain JSON-friendly dicts (no pydantic dependency on slack_api models)
    return [{"id": c.id, "name": c.name} for c in channels]


class PostMessageBody(BaseModel):
    channel_id: str = Field(min_length=1)
    text: str = Field(min_length=1)


@app.post("/messages")
def post_message(
    body: PostMessageBody, client: SlackClient = Depends(get_client)
) -> dict[str, str]:
    msg: Message = client.post_message(channel_id=body.channel_id, text=body.text)

    # Some Message implementations may not have `id`. Create a stable synthetic one.
    message_id = getattr(msg, "id", None)
    if not isinstance(message_id, str) or not message_id:
        message_id = f"{msg.channel_id}:{msg.ts}"

    return {
        "id": message_id,
        "channel_id": msg.channel_id,
        "text": msg.text,
        "ts": msg.ts,
    }