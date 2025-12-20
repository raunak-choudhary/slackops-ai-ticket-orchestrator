# slack-impl

## Overview
`slack-impl` provides a **direct Slack Web API–backed implementation** of the shared `chat_api.ChatInterface`.  
It communicates with Slack’s HTTP APIs, handles OAuth utilities, and manages token storage, while keeping Slack-specific details isolated from the rest of the system.

This module is provider-specific and intentionally separated from adapters and orchestration logic.

## Responsibilities
- Implement `ChatInterface` using the Slack Web API
- Represent Slack messages via the shared `Message` abstraction
- Handle Slack OAuth URL construction and token exchange
- Persist OAuth tokens locally for reuse
- Sanitize and validate message content before sending

## Configuration
For live Slack operations, the following environment variables are required:
- `SLACK_API_BASE_URL`
- `SLACK_BOT_TOKEN`

If these are missing, the client operates in **offline mode**, enabling deterministic behavior for testing.

```python
from slack_impl.slack_client import SlackClient

client = SlackClient()  # reads configuration from environment
```

## How It Works
The implementation is composed of three main parts:
- **SlackClient** — implements `ChatInterface` using Slack HTTP endpoints
- **OAuth helpers** — build authorization URLs and exchange OAuth codes
- **Token store** — persist and reload OAuth tokens using SQLite

```python
client.send_message("C123", "Hello from Slack!")
messages = client.get_messages("C123", limit=5)
```

## Offline vs Online Mode
- **Online mode**: enabled when base URL and token are present
- **Offline mode**: enabled when configuration is missing

Offline mode:
- Avoids network calls
- Returns deterministic stubbed responses
- Simplifies unit testing without Slack credentials

## Dependency Injection
- Importing `slack_impl` registers `SlackClient` with `chat_api.get_client()`
- Application code resolves the active chat client via `chat_api.get_client()`
- Slack-specific logic does not leak outside this module

## Error Handling
- Missing credentials raise `RuntimeError` when live operations are attempted
- Slack API errors are converted into `RuntimeError` or `ConnectionError`
- Provider internals are not exposed upstream

## Testing
Tests verify:
- Dependency injection registration
- Online and offline behavior
- Message send, fetch, and delete operations
- OAuth helper correctness
- Token storage persistence
- Input sanitization

All tests run without requiring live Slack credentials.

## Non-Goals
This module does not:
- Handle Slack Events API payloads
- Perform application-level routing or orchestration
- Abstract Slack workflow concepts beyond chat operations
- Guarantee delivery or message ordering
