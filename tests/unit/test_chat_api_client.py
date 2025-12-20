import pytest
from chat_api.client import ChatInterface


class ConcreteChat(ChatInterface):
    def send_message(self, channel_id: str, content: str) -> bool:
        raise NotImplementedError

    def get_messages(self, channel_id: str, limit: int = 10):
        raise NotImplementedError

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        raise NotImplementedError


def test_chat_interface_methods_raise_not_implemented():
    chat = ConcreteChat()

    with pytest.raises(NotImplementedError):
        chat.send_message("channel", "message")

    with pytest.raises(NotImplementedError):
        chat.get_messages("channel")

    with pytest.raises(NotImplementedError):
        chat.delete_message("channel", "msg-id")
