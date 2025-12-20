import os

import pytest
from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = pytest.mark.integration


def test_chat_to_tickets_create_flow():
    """
    Integration Test:
    Slack -> Orchestrator -> Tickets

    This test verifies that a ticket creation command sent via Slack
    is correctly routed through the Orchestrator to the Tickets flow.

    Passes if no exception is raised.
    """

    # Real Slack test channel ID (must be set in environment)
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="create a ticket for fixing login bug",
        channel=channel_id,
        slack=slack_client,
    )
