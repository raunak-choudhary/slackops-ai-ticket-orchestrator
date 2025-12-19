# Integration Tests – Slack & AI

This document describes the **integration test suite** for the Slack + AI system in the **ospsd-team4-fall2025** project.

Integration tests validate that **multiple components work together correctly**, while still allowing controlled assumptions about external systems.

---

## Scope of Integration Tests

Integration tests cover interactions between the following components:

- Integration App (Orchestrator)
- Slack Adapter
- Slack Service
- AI API
- AI Service
- Dependency Injection & Configuration

These tests sit **between unit tests and E2E tests** in the testing pyramid.

---

##  What Integration Tests Validate

Integration tests ensure that:

- Environment configuration is correct
- Dependency injection resolves properly
- Services communicate over HTTP correctly
- Orchestrator routes commands to the correct handlers
- Slack and AI adapters integrate as expected

They do **not** validate full user flows across all services (that is covered by E2E tests).

---

##  Folder Structure

```
tests/
└── integration/
    ├── test_ai_service_integration.py
    ├── test_config_and_di.py
    ├── test_orchestrator_integration.py
    ├── test_slack_event_handler.py
    ├── test_slack_service_integration.py
```

Each file focuses on a **specific integration boundary**.

---

##  Integration Test Descriptions

| File | Test Name | Description |
|---|---|---|
| `test_ai_service_integration.py` | `test_ai_service_generate_endpoint_live` | Verifies AI Service `/ai/generate` endpoint using live AI |
| `test_config_and_di.py` | `test_config_loads_without_error` | Ensures required environment variables and DI setup |
| `test_orchestrator_integration.py` | `test_orchestrator_ai_command_executes` | Verifies orchestrator routes AI commands correctly |
| `test_slack_event_handler.py` | `test_slack_event_handler_accepts_message_event` | Validates Slack event handling integration |
| `test_slack_service_integration.py` | `test_slack_service_post_and_list_messages` | Confirms Slack Service HTTP APIs work correctly |

---

##  Prerequisites

### Services (must be running)

```bash
uv run uvicorn ai_service.main:app --port 8002
uv run uvicorn slack_service.main:app --port 8001
```

### Required Environment Variables

```bash
export AI_SERVICE_BASE_URL=http://localhost:8002
export SLACK_SERVICE_BASE_URL=http://localhost:8001
export SLACK_TEST_CHANNEL_ID=<REAL_SLACK_CHANNEL_ID>
export OPENAI_API_KEY=sk-...
```

---

##  Running Integration Tests

### Run all integration tests (from repo root)

```bash
uv run pytest tests/integration -m integration -vv
```

### Run a single integration test file

```bash
uv run pytest tests/integration/test_orchestrator_integration.py -vv
```

---

## Expected Output

```text
collected 5 items
5 passed in XX.XXs
```

- No skipped tests
- Live services used where appropriate
- Clean dependency injection

---

##  Integration vs E2E

| Integration Tests | E2E Tests |
|---|---|
| Validate component interactions | Validate full user workflows |
| May assume running services | Exercise complete system |
| Faster and more focused | Slower but more realistic |

Both are required and complementary.

---

##  Summary

- Integration tests validate **service-to-service correctness**
- Each test targets a clear integration boundary
- Tests are runnable locally and suitable for CI
- Combined with E2E tests, they provide full confidence in system behavior

This integration test suite fully satisfies the project testing requirements.
