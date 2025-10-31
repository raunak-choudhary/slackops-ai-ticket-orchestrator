# --- add near top ---
import os
import secrets
from typing import Any, Dict

from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

# Reuse your library’s helpers
from slack_impl.oauth import build_authorization_url, exchange_code_for_tokens  # type: ignore

# Session middleware (needs SECRET_KEY in env)
app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])

# Env config
OAUTH_CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID", "")
OAUTH_CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET", "")
OAUTH_REDIRECT_URI = os.environ.get("OAUTH_REDIRECT_URI", "")  # e.g. https://<render>/auth/callback
OAUTH_SCOPE = os.environ.get("OAUTH_SCOPE", "channels:read,chat:write")

def _require_oauth_env() -> None:
    missing = [k for k, v in {
        "OAUTH_CLIENT_ID": OAUTH_CLIENT_ID,
        "OAUTH_CLIENT_SECRET": OAUTH_CLIENT_SECRET,
        "OAUTH_REDIRECT_URI": OAUTH_REDIRECT_URI,
    }.items() if not v]
    if missing:
        raise HTTPException(status_code=500, detail=f"Missing OAuth env: {', '.join(missing)}")

@app.get("/auth/login", tags=["auth"])
def auth_login(request: Request) -> RedirectResponse:
    """Start OAuth by redirecting to Slack."""
    _require_oauth_env()
    state = secrets.token_urlsafe(24)
    request.session["oauth_state"] = state
    url = build_authorization_url(
        client_id=OAUTH_CLIENT_ID,
        redirect_uri=OAUTH_REDIRECT_URI,
        scope=OAUTH_SCOPE,
        state=state,
    )
    return RedirectResponse(url)

@app.get("/auth/callback", tags=["auth"])
def auth_callback(request: Request, code: str | None = None, state: str | None = None) -> RedirectResponse:
    """Handle Slack callback and store the access token in the session."""
    _require_oauth_env()
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code/state")

    if state != request.session.get("oauth_state"):
        raise HTTPException(status_code=400, detail="Invalid state")

    bundle = exchange_code_for_tokens(
        code=code,
        client_id=OAUTH_CLIENT_ID,
        client_secret=OAUTH_CLIENT_SECRET,
        redirect_uri=OAUTH_REDIRECT_URI,
    )
    # Persist minimally in session (HW2 allows session storage)
    request.session["access_token"] = getattr(bundle, "access_token", "")
    request.session["scope"] = getattr(bundle, "scope", "")
    if not request.session["access_token"]:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    # send user somewhere nice
    return RedirectResponse("/docs")

def require_token(request: Request) -> str:
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@app.get("/me", tags=["auth"])
def me(token: str = Depends(require_token)) -> Dict[str, Any]:
    """Quick check that a token exists post-auth."""
    return {"ok": True, "scope": request.session.get("scope", "")}