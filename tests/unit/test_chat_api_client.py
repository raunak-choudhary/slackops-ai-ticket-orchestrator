import pytest
from chat_api.client import ChatInterface


class ConcreteChat(ChatInterface):
    """
    Concrete test-only implementation to execute
    abstract method bodies for coverage.
    """

    def send_message(self, channel_id: str, content: str) -> bool:
        return super().send_message(channel_id, content)

    def get_messages(self, channel_id: str, limit: int = 10):
        return super().get_messages(channel_id, limit)

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        return super().delete_message(channel_id, message_id)


def test_chat_interface_methods_raise_not_implemented():
    chat = ConcreteChat()

    with pytest.raises(NotImplementedError):
        chat.send_message("channel", "message")

    with pytest.raises(NotImplementedError):
        chat.get_messages("channel")

    with pytest.raises(NotImplementedError):
        chat.delete_message("channel", "msg-id")
