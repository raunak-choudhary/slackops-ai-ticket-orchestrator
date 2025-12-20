import os

import openai_impl  # noqa: F401
import pytest
from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = [pytest.mark.integration, pytest.mark.live]


def test_orchestrator_ai_command_executes():
    """
    Verifies Orchestrator routes 'ai' command and invokes AI + Slack.
    Test passes if no exception is raised.
    """

    # MUST be a real Slack channel ID
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="ai respond with OK",
        channel=channel_id,
        slack=slack_client,
    )
