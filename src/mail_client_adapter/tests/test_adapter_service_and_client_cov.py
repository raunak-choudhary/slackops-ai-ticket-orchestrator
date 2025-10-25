# src/mail_client_adapter/tests/test_adapter_service_and_client_cov.py
from __future__ import annotations

# Import the module so we can monkeypatch its top-level symbols
from mail_client_adapter import adapter
from mail_client_adapter.adapter import AdapterClient, ServiceAdapter


class _ObjWithToDict:
    def to_dict(self):
        return {"id": "obj_2", "sender": "a@example.com", "subject": "hi"}


# ---- ServiceAdapter coverage: exercise list/get/delete/mark paths and _to_plain ----
def test_service_adapter_branches(monkeypatch):
    # Make GeneratedClient a no-op so we don't require the real client package
    class _DummyClient:
        def __init__(self, base_url: str) -> None:
            self.base_url = base_url

    monkeypatch.setattr(adapter, "GeneratedClient", _DummyClient, raising=True)

    # Stub the OpenAPI function objects; each has a .sync we can control
    class _ListAPI:
        @staticmethod
        def sync(**_kwargs):
            # Mixture: plain dict (passes through) + object with .to_dict() (exercises that branch)
            return [
                {"id": "obj_1", "sender": "x@example.com", "subject": "hey"},
                _ObjWithToDict(),
            ]

    class _GetAPI:
        @staticmethod
        def sync(*, message_id: str, **_kwargs):
            # Return dict so adapter returns it as-is
            return {"id": message_id, "sender": "y@example.com", "subject": "yo"}

    class _DeleteAPI:
        @staticmethod
        def sync(**_kwargs):
            # Return a non-dict so adapter falls back to {"id": ..., "deleted": True}
            return 12345

    class _MarkAPI:
        @staticmethod
        def sync(**_kwargs):
            # Return a non-dict so adapter falls back to {"id": ..., "status": "read"}
            return object()

    monkeypatch.setattr(adapter, "api_list_messages", _ListAPI, raising=True)
    monkeypatch.setattr(adapter, "api_get_message", _GetAPI, raising=True)
    monkeypatch.setattr(adapter, "api_delete_message", _DeleteAPI, raising=True)
    monkeypatch.setattr(adapter, "api_mark_as_read", _MarkAPI, raising=True)

    sa = ServiceAdapter(base_url="http://example.test")

    # list_messages: ensure both items are normalized to dicts
    msgs = sa.list_messages()
    assert isinstance(msgs, list)
    assert len(msgs) == 2
    assert msgs[0]["id"] == "obj_1"
    assert msgs[1]["id"] == "obj_2"  # came from .to_dict()

    # get_message: dict passes through
    got = sa.get_message("m_777")
    assert got["id"] == "m_777"

    # delete_message: non-dict -> fallback shape
    deleted = sa.delete_message("m_888")
    assert deleted == {"id": "m_888", "deleted": True}

    # mark_as_read: non-dict -> fallback shape
    marked = sa.mark_as_read("m_999")
    assert marked == {"id": "m_999", "status": "read"}


# ---- AdapterClient coverage: exercise list_emails(), list_messages(limit),
#      and get_email() out-of-bounds path
def test_adapterclient_minimal_contract():
    class _FakeAdapter:
        def list_messages(self, limit: int | None = None):
            _ = limit  # silence ruff ARG002 (we intentionally ignore it)
            # Return empty list to avoid depending on mapping.to_email content
            return []

        def get_message(self, message_id: str):
            return {"id": message_id, "sender": "s@example.com", "subject": "subj"}

        def mark_as_read(self, _message_id: str):
            return {"ok": True}

        def delete_message(self, _message_id: str):
            return {"ok": True}

    client = AdapterClient(adapter=_FakeAdapter())

    # list_emails should handle empty list (covers branch) and return a list
    assert client.list_emails() == []

    # list_messages with a limit also returns empty (covers the limit path)
    assert client.list_messages(limit=1) == []

    # get_email on empty list -> None (covers out-of-bounds branch)
    assert client.get_email(0) is None

    # mark/delete should not raise (no return asserted)
    client.mark_as_read("m_1")
    client.delete_message("m_1")