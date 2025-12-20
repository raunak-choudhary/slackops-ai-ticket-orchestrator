import os

import pytest
from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = pytest.mark.integration


def test_orchestrator_ticket_command_executes():
    """
    Verifies Orchestrator routes ticket creation command.
    Passes if no exception is raised.
    """
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="create a ticket for fixing login bug",
        channel=channel_id,
        slack=slack_client,
    )


def test_orchestrator_ticket_create_alternate_phrase():
    """
    Verifies Orchestrator handles alternate phrasing for ticket creation.
    """
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="open a new ticket for database connection failure",
        channel=channel_id,
        slack=slack_client,
    )


def test_orchestrator_ticket_search_command_executes():
    """
    Verifies Orchestrator routes ticket search command.
    """
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="show my open tickets",
        channel=channel_id,
        slack=slack_client,
    )


def test_orchestrator_ticket_update_command_executes():
    """
    Verifies Orchestrator routes ticket update / close command.
    """
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    orchestrator = Orchestrator()
    slack_client = SlackServiceClient()

    orchestrator.route(
        text="close the most recent ticket",
        channel=channel_id,
        slack=slack_client,
    )
