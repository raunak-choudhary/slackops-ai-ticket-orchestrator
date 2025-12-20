"""
Slack implementation of the ChatInterface protocol.

This module wires SlackClient into chat_api using
explicit environment-based configuration.
"""

import os

import chat_api
from slack_impl.slack_client import SlackClient


def _get_slack_client() -> SlackClient:
    try:
        base_url = os.environ["SLACK_API_BASE_URL"]
        token = os.environ["SLACK_BOT_TOKEN"]
    except KeyError as exc:
        raise RuntimeError(
            f"Missing required Slack environment variable: {exc}"
        ) from exc

    return SlackClient(
        base_url=base_url,
        token=token,
    )


# Dependency injection (FINAL, CORRECT)
chat_api.get_client = _get_slack_client
