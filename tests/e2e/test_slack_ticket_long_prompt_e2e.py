import os
import pytest

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = [pytest.mark.e2e, pytest.mark.live]


def test_long_ticket_description_e2e():
    """
    E2E Test:
    Ticket creation with long descriptive input
    """

    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]
    orchestrator = Orchestrator()
    slack = SlackServiceClient()

    long_text = (
        "create a ticket for a critical production issue where users "
        "experience intermittent failures during checkout, especially "
        "when multiple items are added to the cart over a prolonged session"
    )

    orchestrator.route(
        text=long_text,
        channel=channel_id,
        slack=slack,
    )
