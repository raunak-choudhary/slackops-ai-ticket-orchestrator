from chat_api.chat_api.chat_interface import ChatInterface
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
    def send_message(self, channel_id: str, content: str) -> bool:
        return True

    def get_messages(self, channel_id: str, limit: int = 10):
        return [
            ConcreteMessage("1", "hello", "U1"),
            ConcreteMessage("2", "world", "U2"),
        ]

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        return True


def test_get_messages_integration():
    chat = FakeChatClient()

    messages = chat.get_messages("C_TEST")

    assert isinstance(messages, list)
    assert len(messages) == 2

    for msg in messages:
        assert isinstance(msg, Message)
        assert isinstance(msg.id, str)
        assert isinstance(msg.content, str)
        assert isinstance(msg.sender_id, str)
