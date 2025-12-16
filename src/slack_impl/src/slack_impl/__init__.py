"""Slack implementation of the ChatInterface protocol.

This component provides a concrete implementation of the ChatInterface
using the Slack Web API with OAuth2 authentication.
"""

import chat_api
from slack_impl.slack_client import SlackClient

# Dependency injection: Replace chat_api.get_client with our implementation
chat_api.get_client = lambda: SlackClient()
