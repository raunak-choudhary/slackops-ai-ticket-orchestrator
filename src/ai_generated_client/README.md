# AI Generated Client

This package contains the **auto-generated Python client** for the AI Service,
created directly from the service's OpenAPI specification.

It is **Component 4 of 5** in the AI vertical.

The client is generated using **openapi-python-client**, following the same
process and structure as `slack_generated_client`.

---

## Purpose

The AI generated client allows Python applications and adapters to:

- Call the AI Service over HTTP
- Use strongly-typed request and response models
- Avoid manual HTTP handling
- Stay synchronized with the service API via OpenAPI

This client is **fully generated** and should not contain handwritten logic.

---

## How This Client Is Generated

The client is generated from:

```
src/ai_service/openapi.json
```

using:

```
openapi-python-client
```

Any change to the service routes or models requires **regenerating this client**.

---

## Package Structure

The generated client follows the standard layout produced by
`openapi-python-client`:

- `client.py` — HTTP client configuration
- `api/` — One file per API endpoint
- `models/` — Typed request/response models
- `errors.py` — API error definitions
- `types.py` — Shared type definitions

Supporting files such as `py.typed` enable full static typing support.

---

## What This Package Does NOT Do

This package intentionally excludes:

- Business logic
- Service orchestration
- Dependency injection
- AI provider logic
- FastAPI or server code

It is a **pure client library**.

---

## Tests

Tests validate that:

- The generated client imports correctly
- Public client objects are accessible
- The package is structurally sound

Tests do not perform real HTTP calls.

---

## Role in HW3 Architecture

`ai_generated_client` is **Component 4 of 5** in the AI vertical:

1. ai_api — OSS interface
2. openai_impl — Direct OpenAI implementation
3. ai_service — FastAPI service
4. ai_generated_client — OpenAPI-generated client (this package)
5. ai_adapter — Service-backed adapter

Each component has a single responsibility and must not cross boundaries.

---

## Design Principles

- OpenAPI is the single source of truth
- Generated code is not manually edited
- Strong typing is enforced
- Client and service evolve together
