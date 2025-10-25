from __future__ import annotations

from typing import Protocol


class TokenStore(Protocol):
    """Interface for persisting OAuth tokens. Concrete impl comes later."""
    def upsert(
        self,
        user_id: str,
        access_token: str,
        refresh_token: str | None,
        expires_at: int | None,
        scope: str | None,
    ) -> None: ...
    def get(self, user_id: str) -> dict | None: ...
    def delete(self, user_id: str) -> None: ...
