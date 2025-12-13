from chat_api.chat_api.chat_interface import ChatInterface


class FakeChatClient(ChatInterface):
    def __init__(self):
        self.deleted: list[tuple[str, str]] = []

    def send_message(self, channel_id: str, content: str) -> bool:
        return True

    def get_messages(self, channel_id: str, limit: int = 10):
        return []

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        self.deleted.append((channel_id, message_id))
        return True


def test_delete_message_integration():
    chat = FakeChatClient()

    result = chat.delete_message("C_TEST", "MSG_123")

    assert result is True
    assert chat.deleted == [("C_TEST", "MSG_123")]
