from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import RedirectResponse

# keep your existing oauth helpers
from slack_impl.oauth import build_authorization_url, exchange_code_for_tokens

# ✅ Reuse your existing token store (no duplicates)
from slack_impl.token_store import SQLiteTokenStore, TokenBundle
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Slack Service")
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET", "dev-secret"))


# ---- DB wiring: accept DATABASE_URL or file path ----
def _db_path_from_env() -> str:
    raw = os.environ.get("DATABASE_URL", "sqlite:///./var/slack_tokens.db")
    if raw.startswith("sqlite:///"):
        return raw.replace("sqlite:///", "", 1)
    # Allow passing a plain path like ./var/slack_tokens.db
    return raw


_DB_PATH = _db_path_from_env()
Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)

_store: SQLiteTokenStore | None = None  # single instance


@app.on_event("startup")
def _startup() -> None:
    # Single store instance; your class keeps one connection internally
    global _store
    _store = SQLiteTokenStore(_DB_PATH)


def _get_store() -> SQLiteTokenStore:
    if _store is None:
        raise HTTPException(status_code=500, detail="Token store not initialized")
    return _store


def _require_oauth_env() -> None:
    for k in ("OAUTH_CLIENT_ID", "OAUTH_CLIENT_SECRET", "OAUTH_REDIRECT_URI"):
        if not os.environ.get(k):
            raise HTTPException(status_code=500, detail=f"Missing env: {k}")


# ---- Identity + token dependencies ----
def require_user_id(
    request: Request,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
) -> str:
    uid = request.session.get("user_id") or x_user_id
    if not uid:
        raise HTTPException(status_code=401, detail="No user context; please authenticate")
    return str(uid)


def require_token(
    user_id: str = Depends(require_user_id),
    store: SQLiteTokenStore = Depends(_get_store),
) -> str:
    bundle = store.load(user_id)
    if not bundle or not bundle.access_token:
        raise HTTPException(
            status_code=401, detail="No access token on record; please authenticate"
        )
    return bundle.access_token


# ---- Health: also touches DB lightly ----
@app.get("/health", tags=["infra"])
def health(store: SQLiteTokenStore = Depends(_get_store)) -> dict[str, Any]:
    try:
        _ = store.has("__ping__")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    return {"ok": True}


# ---- OAuth flow ----
@app.get("/auth/login", tags=["auth"])
def auth_login(request: Request) -> RedirectResponse:
    _require_oauth_env()
    state = secrets.token_urlsafe(24)
    request.session["oauth_state"] = state
    url = build_authorization_url(
        client_id=os.environ["OAUTH_CLIENT_ID"],
        redirect_uri=os.environ["OAUTH_REDIRECT_URI"],
        state=state,
        scope="channels:read chat:write users:read",  # adjust to the scopes you really need
    )
    return RedirectResponse(url)


@app.get("/auth/callback", tags=["auth"])
def auth_callback(
    request: Request,
    code: str,
    state: str,
    store: SQLiteTokenStore = Depends(_get_store),
) -> RedirectResponse:
    if state != request.session.get("oauth_state"):
        raise HTTPException(status_code=400, detail="Invalid OAuth state")
    _require_oauth_env()

    bundle = exchange_code_for_tokens(
        code=code,
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        redirect_uri=os.environ["OAUTH_REDIRECT_URI"],
    )

    # Try common Slack shapes; adjust to your actual exchange result
    user_id = getattr(bundle, "authed_user_id", None) or getattr(bundle, "user_id", None)
    if not user_id and hasattr(bundle, "authed_user"):
        user_id = getattr(bundle.authed_user, "id", None)

    access_token = getattr(bundle, "access_token", None)
    refresh_token = getattr(bundle, "refresh_token", None)
    token_type = getattr(bundle, "token_type", "Bearer")
    scope = getattr(bundle, "scope", None)
    expires_at = getattr(bundle, "expires_at", None)

    if not user_id or not access_token:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    # ✅ Persist tokens in DB using your TokenBundle
    store.save(
        str(user_id),
        TokenBundle(
            access_token=str(access_token),
            refresh_token=str(refresh_token) if refresh_token else None,
            token_type=str(token_type or "Bearer"),
            scope=str(scope) if scope else None,
            expires_at=float(expires_at) if isinstance(expires_at, (int, float)) else None,
        ),
    )

    # Keep only identity + optional scope in session (no tokens)
    request.session["user_id"] = str(user_id)
    if scope:
        request.session["scope"] = str(scope)

    return RedirectResponse("/docs")


@app.get("/me", tags=["auth"])
def me(
    request: Request,
    user_id: str = Depends(require_user_id),
    store: SQLiteTokenStore = Depends(_get_store),
) -> dict[str, Any]:
    rec = store.load(user_id)
    return {"ok": True, "user_id": user_id, "scope": (rec.scope if rec else None)}
