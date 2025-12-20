import openai_impl  # noqa: F401

import os
import pytest

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = [pytest.mark.e2e, pytest.mark.live]


def test_ai_and_ticket_commands_together_e2e():
    """
    E2E Test:
    AI request followed by ticket creation
    """

    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]
    orchestrator = Orchestrator()
    slack = SlackServiceClient()

    orchestrator.route(
        text="ai summarize the importance of observability",
        channel=channel_id,
        slack=slack,
    )

    orchestrator.route(
        text="create a ticket for missing metrics dashboard",
        channel=channel_id,
        slack=slack,
    )
