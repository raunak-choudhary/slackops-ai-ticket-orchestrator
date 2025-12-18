from __future__ import annotations

from fastapi.testclient import TestClient

from jira_service.main import app


def test_openapi_schema_has_expected_paths() -> None:
    client = TestClient(app)
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert "/health" in schema["paths"]
    assert "/tickets" in schema["paths"]
    assert "/tickets/{ticket_id}" in schema["paths"]
