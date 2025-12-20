"""Tests for SlackClient.send_message.

These tests validate sending messages via the ChatInterface abstraction.
"""

from unittest.mock import MagicMock

import httpx
import pytest

import chat_api
import slack_impl


@pytest.fixture(autouse=True)
def ensure_slack_injection() -> None:
    """Ensure Slack implementation is injected before each test."""
    import importlib

    importlib.reload(slack_impl)


@pytest.mark.unit
class TestSlackSendMessage:
    """Test cases for sending Slack messages."""

    def test_send_message_offline_returns_true(self) -> None:
        """Offline mode should always succeed."""
        client = chat_api.get_client()

        result = client.send_message("C123", "hello")

        assert result is True

    def test_send_message_online_success(self) -> None:
        """Successful HTTP call returns True."""
        mock_http = MagicMock()
        mock_http.post.return_value = MagicMock(status_code=200)

        client = slack_impl.slack_client.SlackClient(
            base_url="https://slack.test",
            token="xoxb-token",
            http=mock_http,
        )

        result = client.send_message("C123", "hello")

        assert result is True
        mock_http.post.assert_called_once()

    def test_send_message_raises_runtime_error_on_401(self) -> None:
        """401 Unauthorized raises RuntimeError."""
        response = MagicMock(status_code=401)
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=None, response=response
        )

        mock_http = MagicMock()
        mock_http.post.return_value = response

        client = slack_impl.slack_client.SlackClient(
            base_url="https://slack.test",
            token="bad-token",
            http=mock_http,
        )

        with pytest.raises(RuntimeError):
            client.send_message("C123", "hello")

    def test_send_message_raises_connection_error_on_other_http_error(self) -> None:
        """Non-auth HTTP errors raise ConnectionError."""
        response = MagicMock(status_code=500)
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "server error", request=None, response=response
        )

        mock_http = MagicMock()
        mock_http.post.return_value = response

        client = slack_impl.slack_client.SlackClient(
            base_url="https://slack.test",
            token="xoxb",
            http=mock_http,
        )

        with pytest.raises(ConnectionError):
            client.send_message("C123", "hello")
