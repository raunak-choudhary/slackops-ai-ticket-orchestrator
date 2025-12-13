from chat_api.chat_api.chat_interface import ChatInterface
from chat_api.chat_api.message import Message
from ai_impl.ai_impl.openai_client import OpenAIClient
from slack_service.ai_router import poll_and_respond_with_ai


class ConcreteMessage(Message):
    def __init__(self, id: str, content: str, sender_id: str):
        self._id = id
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
    """
    Minimal ChatInterface implementation used only for integration testing.
    """

    def __init__(self):
        self.sent_messages: list[tuple[str, str]] = []

    def send_message(self, channel_id: str, content: str) -> bool:
        self.sent_messages.append((channel_id, content))
        return True

    def get_messages(self, channel_id: str, limit: int = 10):
        return [
            ConcreteMessage(
                id="1",
                content="@team4_ai Say hello in one short sentence.",
                sender_id="U123",
            )
        ]

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        return True


def test_slack_to_openai_to_slack_flow(monkeypatch):
    """
    End-to-end integration test:
    Chat -> AI -> Chat

    OpenAI is mocked to ensure:
    - No real network calls
    - Test is CI-safe
    """

    fake_chat = FakeChatClient()

    # Create OpenAIClient instance WITHOUT calling __init__
    ai_client = OpenAIClient.__new__(OpenAIClient)

    # Mock AI response
    monkeypatch.setattr(
        OpenAIClient,
        "generate_response",
        lambda *_args, **_kwargs: "Hello! This is a mocked AI response.",
    )

    # Required by router
    monkeypatch.setenv("SLACK_CHANNEL_ID", "C_TEST")

    poll_and_respond_with_ai(
        chat_client=fake_chat,
        ai_client=ai_client,
        system_prompt="You are a helpful assistant.",
    )

    assert len(fake_chat.sent_messages) == 1
    channel_id, content = fake_chat.sent_messages[0]

    assert channel_id == "C_TEST"
    assert isinstance(content, str)
    assert "mocked" in content
