# Integration Test Suite

This project includes a comprehensive **integration test suite** that validates configuration wiring, service orchestration, and real service interactions across Slack, AI, and Tickets.

The tests are intentionally split into **local integration tests** (no external services required) and **live integration tests** (require running services). This allows fast local development while still supporting full end‑to‑end validation.

---

## Integration Tests Overview

| Test File | Integration Flow Covered | Services Involved | Live Service Required |
|---------|--------------------------|------------------|----------------------|
| `test_config_and_di.py` | Configuration loading & dependency injection validation | Config loader | No |
| `test_orchestrator_tickets_command.py` | Chat → Tickets (create, search, update) | Orchestrator, Tickets | No |
| `test_slack_tickets_integration.py` | Slack → Tickets via Orchestrator | Slack, Orchestrator, Tickets | No |
| `test_slack_event_handler.py` | Slack event ingestion and routing | Slack Adapter | No |
| `test_orchestrator_integration.py` | Chat → AI → Slack | Orchestrator, AI, Slack | Yes |
| `test_ai_service_integration.py` | Direct AI Service API (`/ai/generate`) | AI Service | Yes |
| `test_slack_service_integration.py` | Direct Slack Service API (post/list messages) | Slack Service | Yes |

---

## Running Integration Tests

### Local Integration Tests (no running services required)

These tests validate orchestration logic and internal integrations without making live HTTP calls.

```bash
uv run pytest -m "integration and not live"
```

---

### Live Integration Tests (services must be running)

These tests validate real HTTP interactions with deployed services.

Required services:
- Slack Service
- AI Service

```bash
uv run pytest -m live
```

---

### Run All Integration Tests

To run **all integration tests together**, ensure all required services are running and environment variables are set, then run:

```bash
uv run pytest
```

---

## Required Environment Variables

```bash
export SLACK_SERVICE_BASE_URL=http://localhost:8001
export AI_SERVICE_BASE_URL=http://localhost:8002
export SLACK_TEST_CHANNEL_ID=<your_slack_channel_id>
export OPENAI_API_KEY=<your_openai_key>
```

---

## Notes

- No mocks or fake services are used.
- Live integration tests perform real HTTP calls.
- Service boundaries are respected via the Orchestrator.
- Configuration issues are detected early through fail‑fast validation.

This structure ensures correctness during development while maintaining confidence in full system integration.
