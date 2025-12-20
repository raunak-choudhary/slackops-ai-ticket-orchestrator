from __future__ import annotations

from fastapi.testclient import TestClient

from jira_service.main import app


def test_health_check() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
