import importlib
from unittest.mock import Mock, patch

import chat_api
import slack_adapter


def setup_function() -> None:
    # Ensure DI runs fresh for each test
    importlib.reload(slack_adapter)


def test_di_injection_returns_service_client(monkeypatch) -> None:
    monkeypatch.setenv("SLACK_SERVICE_BASE_URL", "http://testserver")

    client = chat_api.get_client()
    assert client is not None


def test_get_messages_transforms_response(monkeypatch) -> None:
    monkeypatch.setenv("SLACK_SERVICE_BASE_URL", "http://testserver")

    mock_msg = Mock()
    mock_msg.id = "m1"
    mock_msg.text = "hello"
    mock_msg.sender_id = "u1"

    mock_response = Mock()
    mock_response.messages = [mock_msg]

    with patch(
        "slack_adapter.slack_adapter."
        "list_channel_messages_channels_channel_id_messages_get.sync",
        return_value=mock_response,
    ):
        client = chat_api.get_client()
        messages = client.get_messages("C1")

    assert len(messages) == 1
    assert messages[0].content == "hello"
    assert messages[0].sender_id == "u1"


def test_send_message_success(monkeypatch) -> None:
    monkeypatch.setenv("SLACK_SERVICE_BASE_URL", "http://testserver")

    with patch(
        "slack_adapter.slack_adapter."
        "post_channel_message_channels_channel_id_messages_post.sync",
        return_value=Mock(),
    ):
        client = chat_api.get_client()
        assert client.send_message("C1", "hi") is True
