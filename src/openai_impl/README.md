# openai-impl

## Overview
`openai-impl` provides an OpenAI-backed implementation of the shared `ai_api.AIInterface`.  
It talks directly to the OpenAI SDK and exposes AI capabilities in a way that is fully compliant with the OSS AI contract.

This module is provider-specific and intentionally isolated from the rest of the system.

## Responsibilities
- Implement `AIInterface` using the OpenAI SDK
- Support both conversational and structured (JSON-schema) responses
- Validate presence of required OpenAI credentials
- Sanitize provider errors before propagating them upstream

## Configuration
The OpenAI API key is required and must be provided via environment variable or constructor argument.

Required:
- `OPENAI_API_KEY`

```python
from openai_impl.openai_client import OpenAIClient

client = OpenAIClient()  # reads OPENAI_API_KEY from env
```

Initialization fails fast if no API key is available.

## How It Works
The implementation wraps the OpenAI Chat Completions API and maps responses into the return types defined by `AIInterface`.

```python
response = client.generate_response(
    user_input="Hello",
    system_prompt="Be helpful",
)
```

If a response schema is provided, the client requests strict structured output and returns a dictionary.

## Structured Output
Structured responses use OpenAI’s JSON schema support.

```python
schema = {
    "name": "intent",
    "schema": {
        "type": "object",
        "properties": {"action": {"type": "string"}},
        "required": ["action"],
    },
}

result = client.generate_response(
    user_input="Hi",
    system_prompt="Extract intent",
    response_schema=schema,
)
```

The returned value is a Python dictionary that conforms to the schema.

## Dependency Injection
- Importing `openai_impl` registers this implementation with `ai_api.get_client()`
- Application code resolves the active AI client via `ai_api.get_client()`
- No OpenAI-specific logic leaks outside this module

## Error Handling
- Missing credentials raise `RuntimeError`
- Provider and SDK failures are sanitized into generic `RuntimeError`
- Timeouts and invalid outputs are handled explicitly

Provider internals are never exposed to callers.

## Testing
Tests verify:
- Dependency injection registration on import
- Conversational and structured response handling
- Error sanitization and timeout behavior
- Behavior without real OpenAI calls (SDK is fully mocked)

No tests require a live OpenAI account.

## Non-Goals
This module does not:
- Implement AI routing or orchestration
- Manage prompts beyond direct invocation
- Handle retries, batching, or streaming
- Expose OpenAI SDK objects to callers
