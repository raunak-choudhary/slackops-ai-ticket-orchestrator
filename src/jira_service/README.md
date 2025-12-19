# jira-service

## Overview
`jira-service` is a FastAPI-based HTTP service that exposes ticketing functionality backed by Jira.  
It serves as a **service boundary** between external clients and the Jira-backed ticket implementation, while adhering strictly to the shared `tickets_api` contract.

This service contains no Jira business logic itself.

## Responsibilities
- Expose ticket operations over HTTP
- Activate Jira-backed dependency injection on startup
- Translate HTTP requests into `TicketInterface` calls
- Sanitize and normalize errors into HTTP responses
- Publish OpenAPI documentation for the ticket API

## Application Startup
On startup, the service:
- Creates a FastAPI application
- Imports `jira_impl` to activate ticket dependency injection
- Registers all HTTP routes

```python
import jira_impl  # activates tickets_api.get_client()
```

## HTTP Endpoints

### Health Check
`GET /health`

```json
{ "status": "ok" }
```

Used for liveness and readiness probes.

### Create Ticket
`POST /tickets`

```json
{
  "title": "Bug: login fails",
  "description": "Steps to reproduce...",
  "assignee": "acct_123"
}
```

Returns the created ticket.

### Get Ticket
`GET /tickets/{ticket_id}`

Returns a single ticket or `404` if not found.

### Search Tickets
`GET /tickets?query=foo&status=open`

Returns a list of matching tickets.

### Update Ticket
`PUT /tickets/{ticket_id}`

Supports OSS-compatible updates (title and/or status).

### Delete Ticket
`DELETE /tickets/{ticket_id}`

Deletes a ticket and returns whether the operation succeeded.

## Dependency Injection
- Importing `jira_impl` registers a Jira-backed ticket client
- Routes resolve the active implementation via `tickets_api.get_client()`
- The service remains independent of Jira implementation details

## Error Handling
- Jira connectivity issues return HTTP `503`
- Invalid input returns HTTP `400`
- Missing tickets return HTTP `404`
- Unexpected failures return HTTP `500`
- Provider-specific errors are never leaked

## Testing
Tests verify:
- Health and OpenAPI endpoints
- Request/response model correctness
- Route behavior with injected dummy clients
- Correct HTTP status codes for error cases

All tests run without requiring a live Jira instance.

## Non-Goals
This service does not:
- Contain Jira REST logic
- Manage Jira credentials
- Perform orchestration across services
- Expose provider-specific fields or workflows
