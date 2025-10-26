from __future__ import annotations
from typing import Optional
import os
import urllib.parse
import httpx

from .token_store import TokenBundle

SLACK_OAUTH_AUTHORIZE = "https://slack.com/oauth/v2/authorize"
SLACK_OAUTH_TOKEN     = "https://slack.com/api/oauth.v2.access"

def _get_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env var: {name}")
    return v

def build_authorization_url(state: str) -> str:
    """
    Returns the Slack authorization URL (OAuth 2.0).
    Requires env:
      - SLACK_CLIENT_ID
      - SLACK_REDIRECT_URI
      - SLACK_SCOPES (space-delimited)
    """
    client_id = _get_env("SLACK_CLIENT_ID")
    redirect_uri = _get_env("SLACK_REDIRECT_URI")
    scopes = _get_env("SLACK_SCOPES")

    qs = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "scope": scopes,
            "redirect_uri": redirect_uri,
            "state": state,
        }
    )
    return f"{SLACK_OAUTH_AUTHORIZE}?{qs}"

async def exchange_code_for_tokens(code: str, redirect_uri: Optional[str] = None) -> TokenBundle:
    """
    Exchanges the OAuth 'code' for access/refresh tokens.
    Requires env:
      - SLACK_CLIENT_ID
      - SLACK_CLIENT_SECRET
      - SLACK_REDIRECT_URI (if redirect_uri not passed)
    """
    client_id = _get_env("SLACK_CLIENT_ID")
    client_secret = _get_env("SLACK_CLIENT_SECRET")
    redirect_uri = redirect_uri or _get_env("SLACK_REDIRECT_URI")

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            SLACK_OAUTH_TOKEN,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        # Slack returns { ok, access_token, token_type, scope, ... }
        if not data.get("ok", False):
            raise RuntimeError(f"Slack OAuth failed: {data}")
        return TokenBundle(
            access_token=data.get("access_token", ""),
            refresh_token=None,  # Slack v2 doesn't always give refresh; leave None
            token_type=data.get("token_type", "Bearer"),
            scope=data.get("scope"),
        )

async def refresh_tokens(refresh_token: str) -> TokenBundle:
    """
    Placeholder for token refresh if/when needed.
    Slack typically uses long-lived bot tokens; leave as TODO for Part 4 if required.
    """
    raise NotImplementedError("Slack refresh flow not used; handled by Part 4 if needed.")
