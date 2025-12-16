"""Dependency injection tests for Slack implementation.

These tests verify that importing slack_impl correctly injects
SlackClient into chat_api.get_client().
"""

import importlib

import pytest

import chat_api
import slack_impl
from slack_impl.slack_client import SlackClient


@pytest.mark.unit
class TestSlackDependencyInjection:
    """Verify SlackClient is injected into chat_api."""

    def test_get_client_returns_slack_client_instance(self) -> None:
        """chat_api.get_client should return a SlackClient instance."""
        importlib.reload(slack_impl)

        client = chat_api.get_client()

        assert isinstance(client, SlackClient)
