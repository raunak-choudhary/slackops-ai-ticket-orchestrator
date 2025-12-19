# tickets-api

## Overview
`tickets_api` defines the **provider-agnostic ticketing contract** used across the system.  
It exposes abstract interfaces, shared domain types, and a dependency-injection hook that allow multiple ticket providers (e.g., Jira) to integrate without coupling application code to any specific implementation.

This module contains **no business logic and no provider code**.

## Responsibilities
- Define the canonical `Ticket` domain abstraction
- Define the `TicketInterface` service contract
- Provide a stable `TicketStatus` enumeration
- Expose a dependency injection hook via `get_client()`

## Core Types

### TicketStatus
A shared enumeration of ticket lifecycle states:

```python
from tickets_api.client import TicketStatus

TicketStatus.OPEN
TicketStatus.IN_PROGRESS
TicketStatus.CLOSED
```

These values are intentionally minimal and provider-agnostic.

### Ticket
Abstract base class representing a ticket.

Required properties:
- `id`
- `title`
- `description`
- `status`
- `assignee`

Concrete providers must implement this interface.

### TicketInterface
The service contract implemented by ticket providers.

```python
class TicketInterface(ABC):
    def create_ticket(...)
    def get_ticket(...)
    def search_tickets(...)
    def update_ticket(...)
    def delete_ticket(...)
```

All application code interacts with tickets exclusively through this interface.

## Dependency Injection
`tickets_api` exposes a single DI hook:

```python
from tickets_api import get_client

client = get_client()
```

Implementation packages (e.g., `jira_impl`) **monkey-patch** this function at import time to return their concrete `TicketInterface` implementation.

If no implementation has been registered, calling `get_client()` raises `NotImplementedError`.

## Usage Example

```python
import tickets_api

client = tickets_api.get_client()
ticket = client.create_ticket(
    title="Bug",
    description="Something broke",
)
```

The calling code does not need to know which provider is backing the ticket system.

## Testing Guarantees
Tests in this module verify:
- `TicketInterface` remains abstract
- Dependency injection behavior via monkey-patching
- Public API symbol stability
- Clean imports without side effects

No tests rely on a real ticket provider.

## Design Constraints
This module:
- Must not import any provider implementations
- Must not perform I/O or network operations
- Must remain stable even as providers evolve

Breaking changes here affect all downstream services.

## Non-Goals
`tickets_api` does not:
- Implement ticket storage or workflows
- Validate business rules
- Handle HTTP, databases, or external APIs
- Perform orchestration or routing
