from chat_api.chat_api.chat_interface import ChatInterface


class FakeChatClient(ChatInterface):
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def send_message(self, channel_id: str, content: str) -> bool:
        self.calls.append((channel_id, content))
        return True

    def get_messages(self, channel_id: str, limit: int = 10):
        return []

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        return True


def test_send_message_integration():
    chat = FakeChatClient()

    result = chat.send_message("C_TEST", "Hello from integration test")

    assert result is True
    assert chat.calls == [("C_TEST", "Hello from integration test")]
