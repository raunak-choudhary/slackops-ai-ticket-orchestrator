# ai-service

## Overview
`ai-service` is a FastAPI-based HTTP service that exposes AI capabilities through a stable API.  
It acts as a boundary layer between external clients and the internal AI interface, without depending on any provider-specific implementation.

## Responsibilities
- Expose AI functionality over HTTP
- Activate AI dependency injection at startup
- Translate HTTP requests into `AIInterface` calls
- Sanitize errors before returning responses

## How It Works
On startup, the service activates AI dependency injection by importing an AI implementation.  
At runtime, requests are routed to the currently registered AI client via `ai_api.get_client()`.

```python
import ai_api

client = ai_api.get_client()
result = client.generate_response(
    user_input="hello",
    system_prompt="be helpful",
)
```

The service itself remains unaware of which AI provider is being used.

## HTTP Endpoints

### Generate AI Response
`POST /ai/generate`

```json
{
  "user_input": "Hello",
  "system_prompt": "Be helpful",
  "response_schema": null
}
```

Returns:
```json
{
  "result": "hello"
}
```

Supports both conversational (string) and structured (JSON) responses.

### Health Check
`GET /health`

```json
{
  "status": "healthy"
}
```

## Dependency Injection
- AI providers or adapters register themselves on import
- The service resolves the active AI client dynamically at request time
- No provider-specific logic exists in this module

## Error Handling
- Provider failures are caught and sanitized
- Internal errors are returned as HTTP 500 without leaking implementation details

## Testing
Tests verify:
- Dependency injection is activated on app creation
- HTTP endpoints return correct responses
- Structured and conversational outputs are supported
- Provider failures are handled safely

Tests use mocked AI clients and do not call real providers.
