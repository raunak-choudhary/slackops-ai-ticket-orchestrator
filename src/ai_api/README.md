# ai-api

## Overview
`ai-api` defines the **shared contract** for AI services.  
It standardizes how AI capabilities are invoked while keeping the system independent of any specific AI provider.

This module contains **interfaces only**—no implementations.

## Responsibilities
- Define the abstract `AIInterface`
- Enforce a consistent method signature for AI interactions
- Provide a dependency-injection hook for runtime client resolution

## Interface Contract
All AI implementations must subclass `AIInterface` and implement `generate_response`.

```python
class AIInterface(ABC):
    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict | None = None,
    ) -> str | dict:
        ...
```

### Response Modes
- **Conversational**: returns a `str`
- **Structured**: returns a `dict` matching the provided schema

## Dependency Injection
The module exposes `get_client()` as a runtime injection point.

```python
import ai_api

client = ai_api.get_client()
response = client.generate_response(
    user_input="Hello",
    system_prompt="Be helpful",
)
```

Concrete implementations or adapters are responsible for registering themselves by overriding `get_client`.

## Guarantees
- `AIInterface` cannot be instantiated directly
- Any registered client must fully implement the interface
- Callers remain unaware of provider-specific details

## Testing
Tests validate:
- Abstractness of `AIInterface`
- Enforcement of required methods
- Correct dependency-injection behavior
- Import stability of the public API

No tests in this module interact with real AI providers.

## Non-Goals
This module does not:
- Implement AI providers
- Perform network requests
- Manage configuration or environment variables
- Contain application or business logic
