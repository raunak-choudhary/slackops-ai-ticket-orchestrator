import os
import pytest

from chat_api.chat_api.chat_interface import ChatInterface
from chat_api.chat_api.message import Message
from ai_impl.ai_impl.gemini_client import GeminiClient
from slack_service.ai_router import poll_and_respond_with_ai


class FakeMessage(Message):
    def __init__(self, msg_id: str, content: str, sender_id: str):
        self._id = msg_id
        self._content = content
        self._sender_id = sender_id

    @property
    def id(self) -> str:
        return self._id

    @property
    def content(self) -> str:
        return self._content

    @property
    def sender_id(self) -> str:
        return self._sender_id


class FakeChatClient(ChatInterface):
    def __init__(self):
        self.sent_messages: list[str] = []

    def send_message(self, channel_id: str, content: str) -> bool:
        self.sent_messages.append(content)
        return True

    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]:
        return [
            FakeMessage(
                msg_id="1",
                content="@team4_ai Say hello using Gemini",
                sender_id="user123",
            )
        ]

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        return True


@pytest.mark.integration
def test_ai_router_accepts_gemini_provider():
    """
    Proves that ai_router works with GeminiClient
    (provider selection / swap test).

    This test:
    - Does NOT hit Slack
    - Uses real Gemini if API key exists
    - Skips safely if key is missing
    """

    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set; skipping Gemini router integration test")

    chat_client = FakeChatClient()
    ai_client = GeminiClient()

    poll_and_respond_with_ai(
        chat_client,
        ai_client,
        "fake-channel",
    )

    assert len(chat_client.sent_messages) == 1
    assert isinstance(chat_client.sent_messages[0], str)
    assert chat_client.sent_messages[0].strip() != ""
