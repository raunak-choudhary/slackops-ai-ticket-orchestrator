from __future__ import annotations

from ai_impl import OpenAIClient
from slack_service.ai_router import poll_and_respond_with_ai
from chat_api import ChatInterface, Message


class TerminalMessage(Message):
    def __init__(self, id: str, content: str, sender_id: str) -> None:
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


class TerminalChatClient(ChatInterface):
    """Minimal chat client for manual terminal testing."""

    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]:
        user_input = input("\nType a Slack message: ")
        return [
            TerminalMessage(
                id="local-1",
                content=user_input,
                sender_id="U_LOCAL",
            )
        ]

    def send_message(self, channel_id: str, content: str) -> bool:
        print("\n🤖 AI Response:")
        print(content)
        self.sent_messages.append(content)
        return True

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        # No-op for terminal demo
        print(f"[terminal] delete_message called for {message_id}")
        return True


def main() -> None:
    chat_client = TerminalChatClient()
    ai_client = OpenAIClient()

    print("=== Slack → OpenAI Terminal Demo ===")
    print("Use @team4_ai to trigger the AI\n")

    while True:
        poll_and_respond_with_ai(
            chat_client=chat_client,
            ai_client=ai_client,
            system_prompt="You are a helpful assistant.",
        )


if __name__ == "__main__":
    main()
