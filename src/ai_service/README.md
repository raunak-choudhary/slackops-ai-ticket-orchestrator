# AI Service

This package provides the **FastAPI service layer** for the AI vertical in the OSPSD project.

It is **Component 3 of 5** in the AI vertical and is responsible only for:
- Exposing HTTP endpoints for AI functionality
- Delegating requests to the OSS AI API
- Activating dependency injection for the AI implementation

This service contains **no AI logic itself**.

---

## Purpose

The AI Service translates the OSS AI API into HTTP endpoints so that:
- Other services (e.g., Slack) can call AI functionality over HTTP
- OpenAPI schemas can be generated for client code
- AI providers remain fully decoupled from callers

The service strictly follows the architecture established by `slack_service`.

---

## How It Works

### FastAPI Application

The FastAPI app is defined in `main.py`.

Responsibilities:
- Create the FastAPI application
- Import `openai_impl` to activate dependency injection
- Register routes from `routes.py`
- Expose a `/health` endpoint

No business logic exists in `main.py`.

---

### Routes

Routes are defined in `routes.py`.

The AI endpoint:
- Accepts a request defined by `AIRequest`
- Calls `ai_api.get_client()`
- Delegates execution to the injected AI client
- Returns an `AIResponse`

The service never calls OpenAI directly.

---

### Models

Pydantic models live in `models.py`.

They define:
- Request structure (user input, system prompt, optional schema)
- Response structure (string or structured JSON)

Models are used for:
- Validation
- Documentation
- OpenAPI generation

---

## Dependency Injection

Dependency injection is activated by importing `openai_impl`.

This causes:
- `ai_api.get_client()` to be monkey-patched
- The service to transparently use the OpenAI-backed implementation

The service itself is provider-agnostic.

---

## OpenAPI

The OpenAPI specification lives in `openapi.json`.

It is:
- Generated directly from the FastAPI application
- Used by tests to ensure schema validity
- Used later to generate the AI service client

The file should never be edited manually.

---

## What This Service Does NOT Do

This package intentionally excludes:
- AI provider logic
- OpenAI SDK usage
- Workflow orchestration
- Adapters
- Slack or ticketing integrations

Those responsibilities belong to other components.

---

## Tests

Tests validate:
- Health endpoint availability
- Model correctness
- Route wiring
- OpenAPI schema generation

Tests use real FastAPI wiring and do not mock AI clients.

---

## Role in HW3 Architecture

`ai_service` is **Component 3 of 5** in the AI vertical:

1. ai_api — OSS interface
2. openai_impl — Direct OpenAI implementation
3. ai_service — FastAPI service (this package)
4. ai_generated_client — OpenAPI-generated client
5. ai_adapter — Service-backed adapter

Each component has a single, clearly defined responsibility.

---

## Design Principles

- OSS APIs are the single source of truth
- Services delegate, they do not decide
- Dependency injection is explicit
- Missing configuration fails fast
- Architecture is enforced by tests
