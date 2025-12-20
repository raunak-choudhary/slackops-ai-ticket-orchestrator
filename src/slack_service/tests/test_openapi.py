"""Tests for Slack service OpenAPI schema."""

from fastapi.testclient import TestClient

from slack_service.main import app


def test_openapi_schema_available() -> None:
    """OpenAPI schema endpoint should be available."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "paths" in response.json()
