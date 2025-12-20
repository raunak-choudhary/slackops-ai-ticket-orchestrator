"""Tests for message-related Slack service routes."""

from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from slack_service.main import app


def test_list_messages_success() -> None:
    """GET messages should return transformed messages."""
    client = TestClient(app)

    mock_client = Mock()
    mock_message = Mock()
    mock_message.id = "m1"
    mock_message.content = "hello"
    mock_message.sender_id = "u1"

    mock_client.get_messages.return_value = [mock_message]

    with patch("chat_api.get_client", return_value=mock_client):
        response = client.get("/channels/c1/messages?limit=1")

    assert response.status_code == 200
    data = response.json()

    assert len(data["messages"]) == 1
    assert data["messages"][0]["text"] == "hello"


def test_post_message_success() -> None:
    """POST message should succeed when client returns True."""
    client = TestClient(app)

    mock_client = Mock()
    mock_client.send_message.return_value = True

    with patch("chat_api.get_client", return_value=mock_client):
        response = client.post(
            "/channels/c1/messages",
            json={"text": "hello"},
        )

    assert response.status_code == 200
    assert response.json()["message"]["text"] == "hello"


def test_delete_message_success() -> None:
    """DELETE message should return confirmation."""
    client = TestClient(app)

    mock_client = Mock()
    mock_client.delete_message.return_value = True

    with patch("chat_api.get_client", return_value=mock_client):
        response = client.delete("/channels/c1/messages/m1")

    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
