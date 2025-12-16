"""Tests for the Slack service health endpoint."""

from fastapi.testclient import TestClient

from slack_service.main import app


def test_health_endpoint_returns_ok() -> None:
    """Health endpoint should return service status."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
