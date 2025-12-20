# chat-api

## Overview
`chat-api` defines the shared abstract contract for chat platforms.  
It standardizes how messages are sent, retrieved, and deleted, while keeping the system independent of any specific chat provider (e.g., Slack, Discord, Teams).

This module contains **interfaces only** and no concrete implementations.

## Responsibilities
- Define abstract representations for chat messages
- Define a minimal chat client interface
- Provide a dependency-injection hook for resolving a concrete chat client at runtime

## Interface Contract

### Message
`Message` represents a platform-agnostic chat message.  
Implementations must wrap provider-specific message objects behind this interface.

```python
class Message(ABC):
    @property
    def id(self) -> str: ...
    @property
    def content(self) -> str: ...
    @property
    def sender_id(self) -> str: ...
```

### ChatInterface
`ChatInterface` defines the required operations for interacting with a chat system.

```python
class ChatInterface(ABC):
    def send_message(self, channel_id: str, content: str) -> bool: ...
    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]: ...
    def delete_message(self, channel_id: str, message_id: str) -> bool: ...
```

## Dependency Injection
The module exposes `get_client()` as the injection point for chat implementations.

```python
import chat_api

client = chat_api.get_client()
client.send_message(channel_id="general", content="Hello!")
```

Concrete implementations (e.g., Slack adapters) are responsible for injecting themselves by replacing `get_client`.

If no implementation is injected, calling `get_client()` raises `NotImplementedError`.

## Guarantees
- `Message` and `ChatInterface` cannot be instantiated directly
- Any injected client must fully implement the chat interface
- Application code remains unaware of provider-specific details

## Testing
Tests verify:
- Abstract base class enforcement
- Presence of required interface methods
- Correct dependency-injection behavior
- Public API import stability

Tests do not interact with real chat providers.

## Non-Goals
This module does not:
- Implement chat providers
- Perform network or API calls
- Handle authentication or configuration
- Contain application or business logic
