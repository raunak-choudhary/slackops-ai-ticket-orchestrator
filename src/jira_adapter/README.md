# jira-adapter

## Overview
`jira-adapter` provides a concrete implementation of the shared `TicketInterface` by delegating all ticket operations to a Jira-backed FastAPI service via an auto-generated HTTP client.

It acts as a translation layer between the standardized ticket domain and the Jira service API.

## Responsibilities
- Implement `tickets_api.TicketInterface`
- Delegate ticket operations to the Jira service over HTTP
- Translate service DTOs into domain `Ticket` objects
- Register itself for ticket dependency injection

## How It Works
The adapter uses the generated Jira service client to perform ticket operations and wraps service responses in domain objects that conform to the shared ticket interface.

```python
import tickets_api

client = tickets_api.get_client()
ticket = client.get_ticket("T-123")
```

The adapter itself remains unaware of where or how tickets are ultimately stored.

## Supported Operations
- `create_ticket`
- `get_ticket`
- `search_tickets`

Each operation converts Jira service responses into `Ticket` domain objects.

## Unsupported Operations
The Jira service currently does not expose endpoints for:
- `update_ticket`
- `delete_ticket`

Calling these methods raises `NotImplementedError` to fail fast and clearly.

## Dependency Injection
- The adapter registers itself on import
- The Jira service base URL is read from environment configuration
- Application code resolves the active ticket client via `tickets_api.get_client()`

## Error Handling
- Transport or service failures are wrapped as `ConnectionError`
- Unsupported operations raise explicit `NotImplementedError`
- Provider-specific errors are not leaked to callers

## Testing
Tests verify:
- Correct dependency injection registration
- Proper transformation from service DTOs to domain tickets
- Correct handling of supported operations
- Clean failure for unsupported operations

Tests mock the Jira service client and do not call live services.
