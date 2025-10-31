from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Slack Chat Service (HW2)",
    version="0.1.0",
    description="In-memory FastAPI service used by the adapter tests.",
)

# Simple in-memory data so tests don't hit any external service.
_CHANNELS = [
    {"id": "C001", "name": "general"},
    {"id": "C002", "name": "random"},
]
_msg_counter = 0


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/channels")
def list_channels() -> list[dict[str, str]]:
    return list(_CHANNELS)


class PostMessageBody(BaseModel):
    channel_id: str = Field(min_length=1)
    text: str = Field(min_length=1)


@app.post("/messages")
def post_message(body: PostMessageBody) -> dict[str, str]:
    # Produce a deterministic-ish synthetic id/ts; tests only need shape.
    global _msg_counter
    _msg_counter += 1
    ts = str(_msg_counter)
    mid = f"{body.channel_id}:{ts}"
    return {
        "id": mid,
        "channel_id": body.channel_id,
        "text": body.text,
        "ts": ts,
    }