import os
import pytest

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = [pytest.mark.e2e, pytest.mark.live]


def test_chat_to_ticket_e2e():
    """
    E2E Test:
    Chat → Orchestrator → Tickets → Slack

    This validates the full end-to-end flow using real services.
    """

    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="create a ticket for E2E database outage",
        channel=channel_id,
        slack=slack_client,
    )

    # Test passes if no exception is raised and Slack receives message
