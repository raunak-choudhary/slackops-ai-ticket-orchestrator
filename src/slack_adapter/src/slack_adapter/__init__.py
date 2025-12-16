"""
Slack service-backed adapter injection.

Importing this module injects SlackServiceClient
as the active ChatInterface implementation.
"""

import chat_api
from slack_adapter.slack_adapter import SlackServiceClient

chat_api.get_client = lambda: SlackServiceClient()
