# OpenAI Implementation (openai_impl)

This package provides a **concrete OpenAI-backed implementation** of the OSS AI interface
defined in the `ai_api` package.

It is **Component 2 of 5** in the AI vertical and is responsible for:
- Talking directly to the OpenAI SDK
- Implementing the OSS `AIInterface`
- Activating dependency injection for AI usage

This package contains **no FastAPI code** and **no adapters**.

---

## Purpose

The purpose of `openai_impl` is to provide a **direct provider implementation**
of the AI API using OpenAI.

It translates the abstract AI contract into concrete OpenAI API calls while keeping:
- Provider-specific logic isolated
- Downstream components provider-agnostic

---

## How It Works

### 1. AI Client Implementation

The core logic lives in `openai_client.py`, which defines:

- `OpenAIClient`, a concrete implementation of `AIInterface`
- Direct usage of the OpenAI Python SDK
- Explicit environment variable validation

The client:
- Requires `OPENAI_API_KEY` at initialization
- Raises a `RuntimeError` if the key is missing (TA-mandated behavior)
- Supports both conversational and structured responses

---

### 2. Dependency Injection

Dependency injection is activated when the package is imported.

In `__init__.py`, the package **monkey-patches** the AI API:

- `ai_api.get_client` is replaced
- Calls to `get_client()` return an `OpenAIClient` instance

This mirrors the pattern used in `slack_impl`.

No dependency injection occurs unless `openai_impl` is explicitly imported.

---

## Environment Variables

This package requires the following environment variable:

- `OPENAI_API_KEY` — OpenAI API key used for authentication

Missing environment variables result in **hard failures**, not silent degradation.

---

## What This Package Does NOT Do

This package intentionally excludes:

- FastAPI services
- HTTP endpoints
- Generated OpenAPI clients
- Service-to-service communication
- Adapters or workflow logic

Those responsibilities belong to other components in the AI vertical.

---

## Tests

This package includes tests that enforce:

- Correct dependency injection behavior
- Required environment variable validation
- Compliance with the OSS AI interface

Tests do **not** make real OpenAI API calls and are safe for CI.

---

## Role in HW3 Architecture

`openai_impl` is **Component 2 of 5** in the AI vertical:

1. ai_api — OSS interface
2. openai_impl — Direct OpenAI implementation (this package)
3. ai_service — FastAPI service wrapper
4. ai_generated_client — OpenAPI-generated client
5. ai_adapter — Service-backed adapter

Each component has a single responsibility and must not violate architectural boundaries.

---

## Design Principles

- OSS APIs are the single source of truth
- Provider logic is isolated
- Dependency injection is explicit
- Missing configuration fails fast
