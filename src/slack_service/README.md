# slack-service

## Overview
`slack-service` is a FastAPI-based HTTP service that exposes chat operations backed by Slack.  
It acts as a **pure HTTP adapter** on top of the shared `chat_api.ChatInterface`, translating HTTP requests into chat interface calls and returning provider-agnostic responses.

This service contains **no Slack business logic**.

## Responsibilities
- Expose chat operations over HTTP
- Activate Slack dependency injection via `slack_impl`
- Translate HTTP requests into `ChatInterface` calls
- Convert domain messages into HTTP-safe response models
- Sanitize provider errors into stable HTTP responses
- Publish OpenAPI documentation

## Application Startup
On startup, the service:
- Creates a FastAPI application
- Imports `slack_impl` to activate chat dependency injection
- Registers all Slack service routes

```python
import slack_impl  # activates chat_api.get_client()
```

## HTTP Endpoints

### Health Check
`GET /health`

```json
{ "ok": true }
```

Used for liveness and readiness checks.

### List Channel Messages
`GET /channels/{channel_id}/messages?limit=10`

Returns the most recent messages in a channel.

### Post Message
`POST /channels/{channel_id}/messages`

```json
{
  "text": "hello"
}
```

Posts a message to the given channel.

### Delete Message
`DELETE /channels/{channel_id}/messages/{message_id}`

Deletes a message from a channel.

### List Channel Members
`GET /channels/{channel_id}/members`

Returns a list of channel member identifiers.

## Dependency Injection
- Importing `slack_impl` registers `SlackClient` with `chat_api.get_client()`
- Most routes resolve the active client via `chat_api.get_client()`
- The members endpoint uses `SlackClient` directly for provider-specific access

Slack-specific details do not leak outside this service boundary.

## Error Handling
- Authentication failures → HTTP `401`
- Slack connectivity failures → HTTP `502`
- Missing configuration → HTTP `500`
- Unexpected errors → HTTP `500`

Provider and SDK details are never exposed in responses.

## Models
Pydantic models define the HTTP surface:
- `MessageOut`
- `MessagesResponse`
- `PostMessageIn`
- `PostMessageResponse`
- `MembersResponse`

These models remain provider-agnostic.

## Testing
Tests verify:
- Health and OpenAPI endpoints
- Request/response model validation
- Message list, post, and delete routes
- Member listing behavior
- Correct HTTP status mapping for failures

All tests run without requiring live Slack credentials.

## Non-Goals
This service does not:
- Process Slack Events API payloads
- Perform OAuth flows
- Contain Slack Web API logic
- Perform application orchestration
