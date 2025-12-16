"""Chat API Component.

This component provides abstract interfaces for basic chat client functionality,
following clean architecture principles with dependency injection support.

The interfaces define the contract for chat operations without implementation details,
allowing for multiple chat provider implementations (Slack, Discord, Teams, etc.).

This component focuses on the core requirement: sending, receiving,
and deleting messages across chat platforms.

Example usage:
    from chat_api import ChatInterface, Message

    # Your implementation will inject the actual client
    def process_messages(client: ChatInterface) -> None:
        messages = client.get_messages(channel_id="C123")
        for msg in messages:
            print(msg.content)
"""

from chat_api.client import (
    ChatInterface as ChatInterface,
)
from chat_api.client import (
    Message as Message,
)
from chat_api.client import (
    get_client as get_client,
)

__version__ = "0.1.0"
__description__ = "Chat client interface component"
