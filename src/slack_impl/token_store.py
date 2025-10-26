from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Protocol
import os

# We implement the TokenStore contract from slack_api if present.
try:
    from slack_api import token as token_contract  # e.g., slack_api/token.py
except Exception:
    token_contract = None  # mypy will complain later; Raunak will align imports.

@dataclass(frozen=True)
class TokenBundle:
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    scope: Optional[str] = None

class EnvConfiguredTokenStore(Protocol):
    """Narrow Protocol to satisfy type-checkers if slack_api.TokenStore name differs."""
    def save(self, user_id: str, bundle: TokenBundle) -> None: ...
    def load(self, user_id: str) -> Optional[TokenBundle]: ...

class EnvConfiguredTokenStoreImpl:
    """
    Minimal, env-configured token store.
    - Uses a simple file-backed KV under a folder path from env: SLACK_TOKEN_DIR.
    - This is intentionally simple so Raunak can swap in DB-backed storage later.
    """
    def __init__(self) -> None:
        base = os.getenv("SLACK_TOKEN_DIR")
        if not base:
            raise RuntimeError(
                "SLACK_TOKEN_DIR not set. Set it (or swap to DB-backed store in Part 4)."
            )
        self.base = base
        os.makedirs(self.base, exist_ok=True)

    def _path(self, user_id: str) -> str:
        safe = user_id.replace("/", "_")
        return os.path.join(self.base, f"{safe}.token")

    def save(self, user_id: str, bundle: TokenBundle) -> None:
        with open(self._path(user_id), "w", encoding="utf-8") as f:
            f.write(bundle.access_token or "")
            f.write("\n")
            f.write(bundle.refresh_token or "")
            f.write("\n")
            f.write(bundle.token_type or "Bearer")
            f.write("\n")
            f.write(bundle.scope or "")

    def load(self, user_id: str) -> Optional[TokenBundle]:
        path = self._path(user_id)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f.readlines()]
        access = lines[0] if len(lines) > 0 else ""
        refresh = lines[1] if len(lines) > 1 else None
        ttype   = lines[2] if len(lines) > 2 else "Bearer"
        scope   = lines[3] if len(lines) > 3 else None
        if not access:
            return None
        return TokenBundle(access_token=access, refresh_token=refresh, token_type=ttype, scope=scope)

# Export a name Raunak can DI-bind against easily
TokenStore = EnvConfiguredTokenStoreImpl
