# src/email_api/__init__.py

"""email_api package public API."""

from __future__ import annotations

from .client import Client, Email


def get_client() -> Client:
    """Factory for obtaining an email client (overridable via DI/monkeypatch)."""
    return Client()


__all__ = ["Client", "Email", "get_client"]
