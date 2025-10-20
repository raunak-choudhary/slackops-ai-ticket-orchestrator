# src/gmail_impl/gmail_client.py
from __future__ import annotations

from typing import Any

"""Gmail client implementation (lightweight stub)."""


class GmailClient:
    def ping(self) -> str:
        return "ok"

    def send(self, email: Any) -> str:
        """
        Send an email.

        This is a stub so tests can monkeypatch this method.
        The body is intentionally trivial.
        """
        _ = email
        return "queued"

    def fetch(self, *, limit: int | None = None) -> list[dict[str, Any]]:
        """
        Return a list of message summaries.

        This is a stub to satisfy tests that monkeypatch this method.
        Real implementation would call Gmail API; tests will override it.
        """
        _ = limit  # keep signature & avoid unused warning
        return []