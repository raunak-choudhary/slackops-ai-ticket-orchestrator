from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from typing import List, Optional

from slack_impl import (
    SlackChatClient,
    TokenStore,
    EnvConfiguredTokenStore,
    EnvConfiguredTokenStoreImpl,
    build_authorization_url,
    exchange_code_for_tokens,
)

app = FastAPI(title="Slack Service", version="0.1.0")

def get_token_store() -> TokenStore:
    return EnvConfiguredTokenStoreImpl()

def get_client(store: TokenStore = Depends(get_token_store)) -> SlackChatClient:
    return SlackChatClient(token_store=store)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

# --- OAuth endpoints ---

@app.get("/oauth/authorize")
async def oauth_authorize(state: str = Query(...)) -> dict:
    url = build_authorization_url(state)
    return {"authorize_url": url}

@app.get("/oauth/callback")
async def oauth_callback(code: str = Query(...), state: Optional[str] = None, store: TokenStore = Depends(get_token_store)) -> dict:
    bundle = await exchange_code_for_tokens(code)
    # Use 'state' as correlation key for which user we store against; in practice
    # you might map state->user_id. For now, store under state directly to keep API stable.
    if not state:
        raise HTTPException(status_code=400, detail="Missing state")
    store.save(state, bundle)
    return {"ok": True}

# --- Core chat endpoints (mirror slack_api.ChatClient) ---

@app.get("/channels", response_model=List[dict])
async def list_channels(user_id: str, client: SlackChatClient = Depends(get_client)) -> List[dict]:
    chs = await client.list_channels(user_id=user_id)
    return [{"id": c.id, "name": c.name} for c in chs]

@app.get("/channels/{channel_id}/messages", response_model=List[dict])
async def list_messages(channel_id: str, limit: int = 50, client: SlackChatClient = Depends(get_client)) -> List[dict]:
    msgs = await client.list_messages(channel_id=channel_id, limit=limit)
    return [{"id": m.id, "channel_id": m.channel_id, "text": m.text} for m in msgs]

@app.post("/channels/{channel_id}/messages", response_model=dict)
async def post_message(channel_id: str, text: str, client: SlackChatClient = Depends(get_client)) -> dict:
    msg = await client.post_message(channel_id=channel_id, text=text)
    return {"id": msg.id, "channel_id": msg.channel_id, "text": msg.text}

@app.get("/users/{user_id}", response_model=Optional[dict])
async def get_user(user_id: str, client: SlackChatClient = Depends(get_client)) -> Optional[dict]:
    u = await client.get_user(user_id=user_id)
    if not u:
        return None
    return {"id": u.id, "name": u.name}
