# ai-adapter

## Overview
`ai-adapter` provides a concrete implementation of the shared `AIInterface` by delegating all AI requests to a remote AI service over HTTP. It acts as a thin adapter layer between the core application and the AI service.

## Responsibilities
- Implement the standardized `ai_api.AIInterface`
- Forward AI requests to the AI FastAPI service using an auto-generated client
- Normalize conversational and structured AI responses
- Register itself as the active AI client via dependency injection

## How It Works
The adapter constructs an AI request from user input and system prompts, sends it to the remote AI service, and returns the result. The adapter supports both free-form conversational responses and structured JSON outputs, depending on whether a response schema is provided.

## Configuration
The adapter requires the following environment variable:

- `AI_SERVICE_BASE_URL` — Base URL of the deployed AI service

This variable must be set before calling `register()`.

## Public API
- `AIServiceClient` — Concrete implementation of `AIInterface`
- `register()` — Registers `AIServiceClient` as the active AI client in `ai_api`

## Error Handling
- Raises `ConnectionError` if the AI service is unreachable
- Raises `ConnectionError` if the service returns an empty or invalid response
- Wraps lower-level transport errors to avoid leaking implementation details

## Testing
Unit tests validate:
- Successful client registration
- Conversational (string) responses
- Structured (dictionary) responses
- Proper handling of service failures and empty responses

Tests mock the generated service client to avoid live network calls.

Run tests with:
```bash
pytest
```

## Usage Example
```python
from ai_adapter.ai_adapter import register
import ai_api

register()
client = ai_api.get_client()

response = client.generate_response(
    user_input="Hello",
    system_prompt="Be helpful",
)
```
