# src/mail_client_adapter/tests/test_servicebacked_client_cov.py
from __future__ import annotations

from mail_client_adapter import adapter


def test_servicebackedclient_methods(monkeypatch):
    """
    Cover ServiceBackedClient.fetch_all_emails / fetch_email /
    remove_email / mark_email_as_read without requiring the real generated client.
    """

    class _FakeServiceAdapter:
        def __init__(self, base_url: str = "http://unused") -> None:
            self.base_url = base_url

        def list_messages(self, limit: int | None = None):
            # Return a LIST in both branches
            if limit is None:
                return [{"id": "m_x"}]
            return [{"id": "m_y"}][:limit]

        def get_message(self, message_id: str):
            return {"id": message_id}

        def delete_message(self, message_id: str):
            return {"id": message_id, "deleted": True}

        def mark_as_read(self, message_id: str):
            return {"id": message_id, "status": "read"}

    # Patch the ServiceAdapter referenced by ServiceBackedClient to our fake
    monkeypatch.setattr(adapter, "ServiceAdapter", _FakeServiceAdapter, raising=True)

    # Now when we construct ServiceBackedClient, it will use the fake adapter
    sbc = adapter.ServiceBackedClient(base_url="http://example.test")

    # Exercise all four methods
    assert sbc.fetch_all_emails() == [{"id": "m_x"}]
    assert sbc.fetch_all_emails(limit=1) == [{"id": "m_y"}]
    assert sbc.fetch_email("m_1") == {"id": "m_1"}
    assert sbc.remove_email("m_2") == {"id": "m_2", "deleted": True}
    assert sbc.mark_email_as_read("m_3") == {"id": "m_3", "status": "read"}