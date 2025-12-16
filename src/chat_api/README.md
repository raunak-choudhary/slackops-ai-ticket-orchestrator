# Chat API Component

Chat client interface component for dependency injection and modular architecture.

## Overview

The `chat_api` component provides abstract interfaces for chat client implementations.
It defines contracts without implementation details, enabling clean separation between
chat providers and application logic.

This component follows clean architecture principles and is designed to be used with
dependency injection, allowing multiple chat provider implementations
(e.g., Slack, Discord, Teams) to be swapped without changing user code.

The package is intentionally minimal and focuses only on defining **what** a chat client
must do, not **how** it does it.

## Features

- Abstract Base Class Design: Uses ABCs for explicit implementation contracts
- Provider Agnostic: No platform-specific logic
- Dependency Injection Ready: Implementations inject themselves via `get_client()`
- Type-Safe Interfaces: Compatible with strict static type checking
- Zero Runtime Dependencies: Pure interface definitions only

## Usage

### Basic Interface

```python
from chat_api import ChatInterface, Message

def process_messages(client: ChatInterface) -> None:
    messages = client.get_messages(channel_id="C123", limit=5)
    for msg in messages:
        print(msg.content)
```

### Using Dependency Injection

```python
import chat_api
import slack_impl  # Registers Slack implementation via injection

client = chat_api.get_client()
client.send_message(channel_id="C123", content="Hello world!")
```

## Interface Contract

```python
class ChatInterface(ABC):
    def send_message(self, channel_id: str, content: str) -> bool: ...
    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]: ...
    def delete_message(self, channel_id: str, message_id: str) -> bool: ...
```

## Testing

This component is tested indirectly through integration tests in higher-level
components. As a pure interface package, it contains minimal direct tests.

## License

MIT
