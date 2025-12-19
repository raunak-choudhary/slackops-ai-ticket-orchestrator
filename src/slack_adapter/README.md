# slack-adapter

## Overview
`slack-adapter` provides a concrete implementation of the shared `chat_api.ChatInterface` by delegating all chat operations to a Slack-backed FastAPI service via an auto-generated HTTP client.

It acts as a translation layer between the standardized chat interface and the Slack service.

## Responsibilities
- Implement `ChatInterface`
- Delegate message operations to the Slack service over HTTP
- Translate service responses into domain `Message` objects
- Read required Slack configuration from environment variables

## Configuration
The adapter requires the Slack service base URL to be set at runtime.

Required environment variable:
- `SLACK_SERVICE_BASE_URL`

```python
import os
os.environ["SLACK_SERVICE_BASE_URL"] = "http://localhost:8000"
```

Initialization fails fast if the variable is missing.

## How It Works
The adapter uses the generated Slack service client to invoke message-related endpoints and converts service responses into `Message` objects.

```python
import chat_api

client = chat_api.get_client()
client.send_message("C123", "Hello from Slack adapter")
```

The adapter itself does not depend on the Slack SDK or Slack event payloads.

## Supported Operations
- `send_message`
- `get_messages`
- `delete_message`
- `get_channel_members` (Slack-specific helper)

Standard chat operations return provider-agnostic results.

## Dependency Injection
- Importing `slack_adapter` registers a Slack-backed chat client
- Application code resolves the client via `chat_api.get_client()`
- No Slack-specific logic leaks outside this module

## Error Handling
- Missing configuration raises `RuntimeError`
- Network or service failures raise `ConnectionError`
- Empty or malformed service responses are handled defensively

## Testing
Tests verify:
- Dependency injection registration
- Transformation of service responses into domain messages
- Successful send and fetch operations
- Failure behavior without real Slack calls

All tests mock the Slack service client.

## Non-Goals
This module does not:
- Talk directly to the Slack Web API
- Handle Slack Events API payloads
- Perform orchestration or routing
- Manage Slack authentication or tokens
