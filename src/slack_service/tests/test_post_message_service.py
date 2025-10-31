from __future__ import annotations

from fastapi.testclient import TestClient

from slack_service.app import app


def test_post_message_returns_message_with_ts() -> None:
    client = TestClient(app)
    payload = {"channel_id": "C001", "text": "hello"}
    resp = client.post("/messages", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["channel_id"] == "C001"
    assert data["text"] == "hello"
    assert isinstance(data["id"], str) and data["id"]
    assert isinstance(data["ts"], str) and data["ts"]
