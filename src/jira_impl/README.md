# jira-impl

## Overview
`jira-impl` provides a **direct Jira Cloud–backed implementation** of the shared `tickets_api.TicketInterface`.  
It communicates with Jira’s REST API and maps Jira-specific concepts into the standardized ticket domain used by the rest of the system.

This module is provider-specific and intentionally isolated from higher-level application logic.

## Responsibilities
- Implement `TicketInterface` using Jira Cloud REST APIs
- Load and validate Jira configuration from environment variables
- Translate Jira issues into domain `Ticket` objects
- Encapsulate Jira workflow and payload specifics

## Configuration
Jira configuration is **environment-driven only** and validated at runtime.

Required environment variables:
- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- `JIRA_PROJECT_KEY`

```python
from jira_impl.config import JiraConfig

cfg = JiraConfig.from_env()
```

Missing configuration fails fast with a clear error.

## How It Works
The implementation consists of three layers:
1. **JiraClient** — low-level HTTP client for Jira REST API
2. **JiraTicketClient** — implements `TicketInterface`
3. **JiraTicket** — domain wrapper around Jira issue data

```python
from tickets_api import get_client

client = get_client()
ticket = client.create_ticket("Bug", "Something broke")
```

Jira workflow details (status names, transitions) are normalized before being exposed.

## Status Mapping
Jira workflow statuses are mapped into the shared `TicketStatus` enum:
- Open / To Do → `OPEN`
- In Progress → `IN_PROGRESS`
- Done / Closed → `CLOSED`

Unknown statuses default safely to `OPEN`.

## Dependency Injection
- Importing `jira_impl` registers a Jira-backed ticket client
- Application code resolves tickets via `tickets_api.get_client()`
- No Jira-specific code leaks outside this module

## Error Handling
- Network and transport failures raise `ConnectionError`
- Missing Jira issues return `None` where appropriate
- Invalid inputs raise `ValueError`
- Jira API errors are surfaced with clear runtime exceptions

## Testing
Tests cover:
- Environment configuration validation
- Jira REST client behavior (mocked HTTP)
- Ticket mapping and status normalization
- Full `TicketInterface` compliance without real network calls

No tests require a live Jira instance.

## Non-Goals
This module does not:
- Expose Jira REST details to callers
- Handle Jira workflow transitions generically
- Provide async APIs
- Contain application orchestration logic
