from chat_api.client import ChatClient
from chat_api.chat_impl.slack_chat_client import SlackChatClient


def get_chat_client(token: str) -> ChatClient:
    """
    Factory that returns the correct ChatClient implementation.
    For HW3 (Chat teams), default provider is Slack.
    """
    return SlackChatClient(token)
