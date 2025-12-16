# slack_impl

Slack implementation of the `chat_api` interface.

## Overview

This package provides a concrete implementation of `ChatInterface` backed by the Slack Web API.
It supports OAuth2 authentication, token persistence, and a clean dependency-injection pattern
consistent with the project’s API-first architecture.

The implementation is designed to be used indirectly via `chat_api.get_client()` and should
not be imported or instantiated directly by consumers.

## Features

- Implements `ChatInterface`
- Slack Web API integration
- OAuth2 authorization code flow
- Persistent token storage
- Deterministic offline behavior for tests
- Strict typing with PEP 561 support

## Usage

```python
import chat_api
import slack_impl

client = chat_api.get_client()
client.send_message("C123", "hello world")
messages = client.get_messages("C123", limit=5)
```

## Architecture Notes

- Public surface is limited to `ChatInterface`
- Slack-specific logic is encapsulated within this package
- Dependency injection is performed at import time
- OAuth and token storage are internal implementation details

## Requirements

- Python >= 3.12
- Slack OAuth credentials for online usage

## Development

Run checks from the repository root:

```bash
ruff check .
mypy
pytest
```

## License

This project is intended for academic and educational use.
