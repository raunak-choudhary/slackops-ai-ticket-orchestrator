"""Tests for SlackClient.get_channel_members."""

from unittest.mock import MagicMock

import httpx
import pytest

from slack_impl.slack_client import SlackClient


@pytest.mark.unit
class TestSlackChannelMembers:
    """Test cases for retrieving channel members."""

    def test_get_channel_members_offline_returns_stubbed_members(self) -> None:
        """Offline mode should return deterministic member list."""
        client = SlackClient()

        members = client.get_channel_members("C001")

        assert members == ["U001", "U002"]

    def test_get_channel_members_online_success(self) -> None:
        """Successful Slack API response returns members."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"members": ["U1", "U2", "U3"]}

        mock_http = MagicMock()
        mock_http.get.return_value = mock_response

        client = SlackClient(
            base_url="https://slack.test",
            token="xoxb",
            http=mock_http,
        )

        members = client.get_channel_members("C001")

        assert members == ["U1", "U2", "U3"]

    def test_get_channel_members_raises_runtime_error_on_401(self) -> None:
        """401 Unauthorized raises RuntimeError."""
        response = MagicMock(status_code=401)
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=None, response=response
        )

        mock_http = MagicMock()
        mock_http.get.return_value = response

        client = SlackClient(
            base_url="https://slack.test",
            token="bad-token",
            http=mock_http,
        )

        with pytest.raises(RuntimeError):
            client.get_channel_members("C001")

    def test_get_channel_members_raises_connection_error_on_other_http_error(self) -> None:
        """Non-auth HTTP errors raise ConnectionError."""
        response = MagicMock(status_code=500)
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "server error", request=None, response=response
        )

        mock_http = MagicMock()
        mock_http.get.return_value = response

        client = SlackClient(
            base_url="https://slack.test",
            token="xoxb",
            http=mock_http,
        )

        with pytest.raises(ConnectionError):
            client.get_channel_members("C001")
