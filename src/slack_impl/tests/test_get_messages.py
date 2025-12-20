"""Tests for SlackClient.get_messages.

These tests validate message retrieval behavior.
"""

from unittest.mock import MagicMock

import httpx
import pytest

import chat_api
import slack_impl
from slack_impl.slack_client import SlackMessage


@pytest.fixture(autouse=True)
def ensure_slack_injection() -> None:
    """Ensure Slack implementation is injected before each test."""
    import importlib

    importlib.reload(slack_impl)


@pytest.mark.unit
class TestSlackGetMessages:
    """Test cases for retrieving Slack messages."""

    def test_get_messages_offline_returns_stubbed_messages(self) -> None:
        """Offline mode returns deterministic messages."""
        client = chat_api.get_client()

        messages = client.get_messages("C001", limit=2)

        assert len(messages) == 2
        assert isinstance(messages[0], SlackMessage)
        assert messages[0].content == "hello"

    def test_get_messages_limit_zero_returns_empty(self) -> None:
        """Limit=0 returns empty list."""
        client = chat_api.get_client()

        messages = client.get_messages("C001", limit=0)

        assert messages == []

    def test_get_messages_online_success(self) -> None:
        """Successful Slack API response is parsed."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "messages": [
                {"text": "hello", "ts": "1", "user": "U1"},
                {"text": "world", "ts": "2", "user": "U2"},
            ]
        }

        mock_http = MagicMock()
        mock_http.get.return_value = mock_response

        client = slack_impl.slack_client.SlackClient(
            base_url="https://slack.test",
            token="xoxb",
            http=mock_http,
        )

        messages = client.get_messages("C001", limit=10)

        assert len(messages) == 2
        assert messages[0].content == "hello"
        assert messages[1].sender_id == "U2"

    def test_get_messages_raises_runtime_error_on_403(self) -> None:
        """403 Forbidden raises RuntimeError."""
        response = MagicMock(status_code=403)
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "forbidden", request=None, response=response
        )

        mock_http = MagicMock()
        mock_http.get.return_value = response

        client = slack_impl.slack_client.SlackClient(
            base_url="https://slack.test",
            token="bad-token",
            http=mock_http,
        )

        with pytest.raises(RuntimeError):
            client.get_messages("C001")

    def test_get_messages_raises_connection_error_on_generic_exception(self) -> None:
        """Generic exceptions raise ConnectionError."""
        mock_http = MagicMock()
        mock_http.get.side_effect = Exception("network down")

        client = slack_impl.slack_client.SlackClient(
            base_url="https://slack.test",
            token="xoxb",
            http=mock_http,
        )

        with pytest.raises(ConnectionError):
            client.get_messages("C001")
