"""Tests for channel-related Slack service routes."""

from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from slack_service.main import app


def test_list_channel_members_success() -> None:
    """GET channel members should return member list."""
    client = TestClient(app)

    mock_client = Mock()
    mock_client.get_channel_members.return_value = ["u1", "u2"]

    with patch("chat_api.get_client", return_value=mock_client):
        response = client.get("/channels/c1/members")

    assert response.status_code == 200
    assert response.json()["members"] == ["u1", "u2"]
