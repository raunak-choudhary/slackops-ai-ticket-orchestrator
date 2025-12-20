# integration-app

## Overview
`integration-app` is the main entry point for the HW3 system integration.  
It wires together Slack, AI, and supporting services into a single FastAPI application that handles real user events and routes them through the system.

This module is responsible for **orchestration**, not business logic.

## Responsibilities
- Validate required runtime configuration
- Activate dependency injection for adapters
- Expose the Slack Events API endpoint
- Route incoming Slack messages to the orchestrator
- Coordinate cross-vertical interactions

## Application Startup
On startup, the application:
- Loads and validates required environment variables
- Activates AI adapter dependency injection
- Initializes the FastAPI application

```python
from integration_app.config import load_config

load_config()
```

If required configuration is missing, startup fails fast with a clear error.

## Slack Events Endpoint
The application exposes a Slack Events API endpoint:

```
POST /slack/events
```

This endpoint:
- Handles Slack URL verification handshakes
- Accepts message events
- Delegates processing to the Slack event handler

## Orchestration Flow
Incoming Slack messages are routed through the `Orchestrator`, which:
- Performs deterministic command parsing
- Explicitly handles supported commands
- Delegates AI-related commands to the AI service
- Sends responses back to Slack via the adapter

```python
orchestrator.route(text, channel, slack_client)
```

The orchestrator contains no Slack SDK logic and no provider-specific code.

## Dependency Injection
- AI dependency injection is activated explicitly at import time
- Slack clients are instantiated per request
- All integrations rely on shared APIs rather than concrete providers

## Error Handling
- Configuration errors fail fast during startup
- Slack events are acknowledged even when commands are ignored
- Provider failures are logged without crashing the application

## Testing and Usage
This module is intended to be run as the main application service.
It is exercised primarily through integration and end-to-end tests rather than isolated unit tests.

## Non-Goals
This module does not:
- Implement Slack or AI providers
- Contain AI or ticketing business logic
- Perform long-running background processing
- Replace individual service responsibilities
