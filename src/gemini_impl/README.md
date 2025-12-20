# Gemini AI Provider

This module provides a minimal implementation of the shared **AI vertical**
using Google Gemini as an additional provider.

The purpose of this implementation is to demonstrate **support for multiple
providers within the same AI vertical**, alongside the existing OpenAI-based
implementation, while continuing to use the standardized `AIInterface`
defined in `ai_api`.

---

## Overview

- Implements the shared `AIInterface`
- Uses environment variables for configuration
- Supports both conversational and structured (schema-based) responses
- Includes unit tests
- Designed to be swappable with other AI providers without changing
  orchestration logic

This provider intentionally keeps the implementation lightweight and reuses
the existing AI service and API layers.

---

## Project Structure

```
src/gemini_impl
├── README.md
├── pyproject.toml
├── src
│   └── gemini_impl
│       ├── __init__.py
│       ├── client.py
│       ├── config.py
│       ├── errors.py
│       └── provider.py
└── tests
    ├── __init__.py
    └── test_gemini_provider.py
```

---

## Environment Variables

The following environment variables must be defined (e.g. in `.env`):

```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-pro
```

- `GEMINI_API_KEY` is required
- `GEMINI_MODEL` is optional and defaults to `gemini-1.5-pro`

---

## Usage Example

```python
from gemini_impl import GeminiProvider

provider = GeminiProvider()

response = provider.generate_response(
    user_input="Hello",
    system_prompt="You are a helpful assistant",
)

print(response)
```

### Structured Response Example

```python
schema = {"type": "object"}

response = provider.generate_response(
    user_input="Create a ticket for login bug",
    system_prompt="Extract intent",
    response_schema=schema,
)
```

---

## Testing

Run unit tests with:

```bash
uv run pytest src/gemini_impl/tests
```

The tests validate:
- Environment variable loading
- Conversational responses
- Structured (schema-based) responses

No external API calls are made during testing.

---

## Design Notes

- This provider directly implements the shared `AIInterface`
- No provider-specific logic leaks into the shared API layer
- The existing AI service and orchestration layers remain unchanged
- Demonstrates provider swappability within the AI vertical

---

## Purpose in HW3

This implementation satisfies the HW3 requirement to demonstrate
**integration with multiple providers from the same vertical**, while
maintaining clean abstractions and minimal duplication.
