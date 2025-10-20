# src/mail_client_adapter/tests/test_adapterclient_contract.py
from __future__ import annotations

from typing import Any

import mail_client_adapter.backed_client as bc
from email_api import (
    Client as EmailApiClient,
)


class _FakeAdapter:
    """Minimal stand-in for ServiceAdapter so we avoid any network calls."""
    def __init__(self, base_url: str = "http://does-not-matter") -> None:  # noqa: ARG002
        self._messages: list[dict[str, Any]] = [
            {
                "id": "m_1",
                "subject": "hi",
                "from": "a@example.com",
                "to": "b@example.com",
                "read": False,
            },
            {
                "id": "m_2",
                "subject": "yo",
                "from": "c@example.com",
                "to": "d@example.com",
                "read": True,
            },
        ]

    def list_messages(self, limit: int | None = None) -> list[dict[str, Any]]:
        data = self._messages
        return data if limit is None else data[:limit]

    def get_message(self, message_id: str) -> dict[str, Any]:
        for m in self._messages:
            if m["id"] == message_id:
                return m
        raise KeyError(message_id)

    def delete_message(self, message_id: str) -> dict[str, Any]:
        for i, m in enumerate(self._messages):
            if m["id"] == message_id:
                self._messages.pop(i)
                return {"ok": True}
        return {"ok": False}

    def mark_as_read(self, message_id: str) -> dict[str, Any]:
        for m in self._messages:
            if m["id"] == message_id:
                m["read"] = True
                return {"ok": True}
        return {"ok": False}


def test_adapterclient_contract(monkeypatch):
    # Monkeypatch the ServiceAdapter used inside AdapterClient to avoid network.
    monkeypatch.setattr(bc, "ServiceAdapter", _FakeAdapter)

    client: EmailApiClient = bc.AdapterClient(adapter=_FakeAdapter())
    assert isinstance(client.list_emails(), list)
    assert client.get_email(0) is not None