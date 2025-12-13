from chat_api.chat_api.message import Message
from chat_api.chat_api.chat_interface import ChatInterface
from ai_impl import OpenAIClient
from slack_service.ai_router import poll_and_respond_with_ai
from chat_api.chat_api.message import Message


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
    def __init__(self):
        self.sent_messages = []

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
    fake_chat = FakeChatClient()
    ai_client = OpenAIClient()

    # inject env var safely
    monkeypatch.setenv("SLACK_CHANNEL_ID", "C_TEST")

    poll_and_respond_with_ai(
        chat_client=fake_chat,
        ai_client=ai_client,
        system_prompt="You are a helpful assistant.",
    )

    assert len(fake_chat.sent_messages) == 1
    channel, content = fake_chat.sent_messages[0]
    assert channel == "C_TEST"
    assert isinstance(content, str)
    assert len(content) > 0
