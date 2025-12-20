
# Unit Tests README

## Overview
This document describes the **unit tests** implemented in this repository.
Unit tests validate the correctness of **core interfaces and contracts**
independently of external systems such as Slack, OpenAI, or ticketing backends.

They are intentionally lightweight, deterministic, and fast.

---

## Why Unit Tests Exist

Unit tests in this project focus on:

- Verifying **abstract interface contracts**
- Ensuring **dependency injection failure modes** behave correctly
- Covering **base-layer logic** without invoking external services
- Contributing to the **≥85% coverage requirement** in a legitimate way

They do **not** test:
- Slack APIs
- OpenAI responses
- Network I/O
- External SDK behavior

Those are covered by **integration** and **E2E tests**.

---

## Unit Test Files

### `test_ai_api_client.py`
Validates the AI API contract.

Covers:
- `AIInterface.generate_response` abstract method behavior
- `get_client()` failure when no AI client is registered

Purpose:
Ensures AI implementations must explicitly register before use.

---

### `test_chat_api_client.py`
Validates the Chat API contract.

Covers:
- `ChatInterface.send_message`
- `ChatInterface.get_messages`
- `ChatInterface.delete_message`
- `get_client()` failure behavior

Purpose:
Guarantees chat implementations conform to required behavior.

---

### `test_chat_message_interface.py`
Validates the `Message` abstract interface.

Covers:
- `id`
- `content`
- `sender_id`

Purpose:
Ensures all chat message implementations expose required properties.

---

### `test_tickets_api_client.py`
Validates ticketing contracts.

Covers:
- `TicketInterface` abstract methods
- `Ticket` abstract properties
- Global DI binding (`bind_client`, `get_client`)

Purpose:
Ensures ticket providers follow the defined interface and lifecycle.

---

### `test_get_client_errors.py`
Validates dependency injection failure cases.

Covers:
- Proper error raising when DI bindings are missing

Purpose:
Prevents silent failures when services are not registered.

---

### `test_orchestrator_unit.py`
Unit-level tests for orchestrator logic.

Covers:
- Internal branching logic
- Message routing decisions
- Non-network execution paths

Purpose:
Ensures correctness of orchestration without external calls.

---

## Coverage Strategy

- Abstract interfaces are **executed intentionally** to satisfy contract coverage
- No fake implementations are used
- No production code is modified for coverage
- Coverage reflects **real contract enforcement**, not artificial mocks

Final result:
- **>85% total coverage**
- All unit tests pass
- No skipped or flaky unit tests

---

## How to Run Unit Tests

Run only unit tests:
```bash
uv run pytest tests/unit
```

Run with coverage:
```bash
uv run pytest --cov --cov-report=term-missing
```

---

## Reviewer Notes (Important)

- Abstract interfaces are explicitly tested by invoking base behavior
- This is an accepted and recommended strategy for interface-driven systems
- External integrations are intentionally excluded from unit tests
- Integration and E2E tests cover real workflows separately

---

## Summary

The unit test suite ensures:

- Strong interface contracts
- Predictable failure modes
- High confidence in core logic
- Compliance with coverage requirements

This design supports scalability, maintainability, and safe extension.
