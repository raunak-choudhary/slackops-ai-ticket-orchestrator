import os
import pytest

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = [pytest.mark.e2e, pytest.mark.live]


def test_non_ticket_message_e2e():
    """
    E2E Test:
    Non-ticket message should not create a ticket
    """

    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]
    orchestrator = Orchestrator()
    slack = SlackServiceClient()

    orchestrator.route(
        text="hello team, how are things going today?",
        channel=channel_id,
        slack=slack,
    )
