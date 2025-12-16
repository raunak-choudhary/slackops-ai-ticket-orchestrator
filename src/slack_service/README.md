# Slack Service

FastAPI-based HTTP service that exposes chat operations through the abstract
`chat_api` interface using dependency injection.

## Overview

This service acts as a server-side adapter. It translates HTTP requests into
calls against the provider-agnostic `ChatInterface`, with the concrete Slack
implementation injected at import time.

The service contains no Slack SDK logic, OAuth handling, token storage, or AI
features. All provider-specific behavior lives in `slack_impl`.

## Architecture

- chat_api: Interface layer (contracts only)
- slack_impl: Slack provider implementation (injected)
- slack_service: HTTP adapter (this component)

## Key Principles

- Provider-agnostic service layer
- Dependency injection via import side effects
- Thin, deterministic FastAPI routes
- Strict typing and clean separation of concerns
- TA-aligned structure and conventions

## Running Locally

From the repository root:

```bash
uv sync --all-packages --dev
uv run python -m slack_service.main
```

The service will be available at:

- http://localhost:8000/docs
- http://localhost:8000/openapi.json

## Development

Run tests from the component root:

```bash
pytest
```

## Notes

This project is intended for academic use as part of the OSPSD coursework.
