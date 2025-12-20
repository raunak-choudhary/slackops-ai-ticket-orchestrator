import os
import pytest

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = [pytest.mark.e2e, pytest.mark.live]


def test_multiple_ticket_creations_e2e():
    """
    E2E Test:
    Multiple chat → ticket commands in sequence
    """

    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]
    orchestrator = Orchestrator()
    slack = SlackServiceClient()

    messages = [
        "create a ticket for database latency issue",
        "create a ticket for login timeout bug",
        "create a ticket for payment gateway failure",
    ]

    for msg in messages:
        orchestrator.route(
            text=msg,
            channel=channel_id,
            slack=slack,
        )
