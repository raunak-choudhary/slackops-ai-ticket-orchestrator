# Slack Generated Service API Client

This package contains the auto-generated Python client for the Slack Service API.
It is generated from the OpenAPI specification exposed by the `slack_service`
component using `openapi-python-client`.

This client **does not communicate with Slack directly**. It only talks to the
Slack Service (FastAPI) over HTTP and acts as a low-level transport layer for
higher-level adapters.

---

## Overview

The Slack Generated Client is:

- Fully auto-generated from OpenAPI
- Type-safe and mypy-friendly
- Provider-agnostic (no Slack SDK usage)
- Synchronous and asynchronous (we use sync variants)
- Free of business logic, dependency injection, or adapters

Architectural position:

chat_api  
↑  
slack_impl  
↑  
slack_service (FastAPI)  
↑  
slack_generated_client (this package)

---

## Installation

This package is part of the workspace and is installed automatically via `uv`:

```bash
uv sync
```

No separate installation step is required.

---

## Usage

This client is primarily consumed internally by higher-level adapters.
Direct usage is generally unnecessary, but an example is shown below for reference.

### Direct Usage Example

```python
from slack_service_api_client import Client
from slack_service_api_client.api.default import (
    list_channel_messages_channels_channel_id_messages_get,
)

client = Client(base_url="http://localhost:8000")

with client as c:
    response = list_channel_messages_channels_channel_id_messages_get.sync(
        client=c,
        channel_id="C123",
        limit=10,
    )
    if response:
        for message in response.messages:
            print(message.content)
```

---

## API Function Variants

For each endpoint, the generated client provides four variants:

1. `sync()` – blocking call returning parsed data (used by adapters)
2. `sync_detailed()` – blocking call returning full HTTP response
3. `asyncio()` – async call returning parsed data
4. `asyncio_detailed()` – async call returning full HTTP response

Only synchronous variants are used in our system because the
`chat_api.ChatInterface` is synchronous.

---

## Available Endpoints

- **GET /health**
  - Function: `health_check_health_get.sync(client)`
  - Returns: Health status response

- **GET /channels/{channel_id}/messages**
  - Function: `list_channel_messages_channels_channel_id_messages_get.sync(...)`
  - Returns: MessagesResponse

- **POST /channels/{channel_id}/messages**
  - Function: `post_channel_message_channels_channel_id_messages_post.sync(...)`
  - Returns: PostMessageResponse

- **DELETE /channels/{channel_id}/messages/{message_id}**
  - Function: `delete_channel_message_channels_channel_id_messages_message_id_delete.sync(...)`
  - Returns: Deletion status

- **GET /channels/{channel_id}/members**
  - Function: `list_channel_members_channels_channel_id_members_get.sync(...)`
  - Returns: MembersResponse

---

## Models

All response and request models are available under:

```python
slack_service_api_client.models
```

Examples include:

- `MessageOut`
- `MessagesResponse`
- `MembersResponse`
- `PostMessageIn`
- `PostMessageResponse`
- `HealthResponse`

All models use `attrs` and are fully typed.

---

## Regeneration

If the Slack Service API changes, this client must be regenerated.

### Prerequisites

If `openapi-python-client` is not installed:

```bash
brew install pipx
pipx install openapi-python-client
pipx ensurepath
```

If the command is not found, ensure the following is in your shell config:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Generate OpenAPI Spec

```bash
python - << 'EOF'
from slack_service.main import app
import json
from pathlib import Path

path = Path("src/slack_service/openapi.json")
path.write_text(json.dumps(app.openapi(), indent=2))
EOF
```

### Regenerate Client

```bash
openapi-python-client generate   --path src/slack_service/openapi.json   --output-path src/slack_generated_client   --overwrite
```

---

## Notes

- This is an auto-generated client; do not manually edit generated files
- Uses `httpx` for HTTP communication
- Uses `attrs` for models
- Includes `py.typed` for static type checking
- Formatting warnings during generation (e.g. missing `ruff`) are safe to ignore
