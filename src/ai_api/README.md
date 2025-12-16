# AI API

This package defines the **OSS-standardized abstract interface** for AI systems used in the OSPSD project.

It contains **interfaces only** and deliberately includes **no implementation logic**. All concrete behavior must be provided by other components via dependency injection.

This package is the **single source of truth** for how AI functionality is consumed by the rest of the system.

---

## Purpose

The AI API defines the minimal contract required for interacting with an AI system:

- Accepting user input  
- Accepting a system prompt  
- Optionally requesting structured (schema-based) output  
- Returning either a conversational response or structured data  

The interface is intentionally small and stable to allow multiple AI providers and architectures to coexist without downstream changes.

---

## Core Interface

### AIInterface

AIInterface is an **abstract base class** that all AI implementations must extend.

It defines exactly one required method:

generate_response(  
    user_input: str,  
    system_prompt: str,  
    response_schema: dict | None = None,  
) -> str | dict

### Contract Rules (Enforced by Tests)

- AIInterface **cannot be instantiated directly**
- Any concrete implementation **must** implement `generate_response`
- The method signature must match exactly
- The return value must be:
  - a string for conversational output, or
  - a dictionary for structured output when a schema is provided

Any deviation from this contract will cause tests to fail.

---

## Dependency Injection

This package exposes a `get_client()` function used to retrieve the active AI client.

### Behavior

- By default, calling `get_client()` raises a RuntimeError
- An implementation must explicitly register itself by overriding `get_client`
- This prevents accidental usage without a configured AI backend

Registration is performed by:
- a concrete implementation (for example, `openai_impl`), or
- a service-backed adapter (for example, `ai_adapter`)

---

## What This Package Does NOT Contain

This package intentionally excludes:

- Concrete AI implementations  
- HTTP or FastAPI code  
- Environment variable access  
- Provider-specific logic  
- Response wrapper classes or extra abstractions  

All such logic belongs in other components.

---

## Test Coverage

The following guarantees are enforced by tests:

- The interface is abstract
- Abstract methods are required
- Dependency injection fails safely when not configured
- Public imports are stable and intentional
- Concrete implementations must comply with the OSS contract

If any architectural boundary is violated, tests will fail.

---

## Role in HW3 Architecture

This package is **Component 1 of 5** in the AI vertical:

1. ai_api — OSS interface (this package)  
2. openai_impl — Concrete AI implementation  
3. ai_service — FastAPI service wrapping the implementation  
4. ai_generated_client — Auto-generated OpenAPI client  
5. ai_adapter — Service-backed adapter implementing AIInterface  

Each component has a single responsibility and must not cross boundaries.

---

## Design Principles

- OSS APIs are the **single source of truth**
- Interfaces are **minimal and stable**
- Dependency injection is **explicit and enforced**
- Tests define and protect the architecture
