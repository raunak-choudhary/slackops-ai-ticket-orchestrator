"""Tests for channel-related Slack service routes.

"""

from fastapi.testclient import TestClient
from unittest.mock import patch

from slack_service.main import app

client = TestClient(app)


def test_list_channel_members_success() -> None:
    """Successfully list members of a Slack channel."""
    with patch(
        "slack_service.routes.SlackClient.get_channel_members",
        return_value=["U001", "U002", "U003"],
    ):
        response = client.get("/channels/C123/members")

    assert response.status_code == 200
    data = response.json()
    assert data == {"members": ["U001", "U002", "U003"]}


def test_list_channel_members_auth_failure() -> None:
    """Authentication failures should return 401."""
    with patch(
        "slack_service.routes.SlackClient.get_channel_members",
        side_effect=RuntimeError("auth failed"),
    ):
        response = client.get("/channels/C123/members")

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Slack authentication failed while listing channel members"
    )


def test_list_channel_members_connection_failure() -> None:
    """Connection failures should return 502."""
    with patch(
        "slack_service.routes.SlackClient.get_channel_members",
        side_effect=ConnectionError("network error"),
    ):
        response = client.get("/channels/C123/members")

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Unable to reach Slack while listing channel members"
    )
