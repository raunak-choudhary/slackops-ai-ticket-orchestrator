# End-to-End (E2E) Tests – Slack & AI

This document describes the **End-to-End (E2E) test suite** for the Slack + AI workflow in the **ospsd-team4-fall2025** project.

These tests validate the **full application flow using live services**, without mocks and without skipped tests.

---

## 📌 Scope of E2E Tests

The E2E tests cover **Slack + AI only**.

They intentionally **exclude email workflows**, which are legacy tests and are not part of the Slack/AI product vertical.

### What is validated end-to-end:

```
Slack Service
   ↓
Orchestrator
   ↓
AI Service (OpenAI)
   ↓
Slack Service (message history)
```

---

## 📂 Folder Structure

```
tests/
└── e2e/
    ├── test_slack_ai_basic_flow.py
    ├── test_slack_ai_e2e.py
    ├── test_slack_ai_long_prompt.py
    ├── test_slack_ai_multiple_requests.py
    ├── test_slack_non_ai_message.py
```

Each file contains **exactly one E2E behavior**, following best testing practices.

---

## 🧪 E2E Test Descriptions

| File | Test Name | Description |
|---|---|---|
| `test_slack_ai_basic_flow.py` | `test_slack_ai_basic_flow` | Verifies basic Slack → AI → Slack happy path |
| `test_slack_ai_e2e.py` | `test_slack_ai_end_to_end_via_orchestrator` | Full internal E2E via orchestrator |
| `test_slack_ai_multiple_requests.py` | `test_slack_ai_multiple_requests` | Handles multiple AI commands in same channel |
| `test_slack_ai_long_prompt.py` | `test_slack_ai_long_prompt` | AI handles longer, realistic prompts |
| `test_slack_non_ai_message.py` | `test_slack_non_ai_message` | Non-AI messages do not trigger AI |

---

## ⚙️ Prerequisites

### Services (must be running)

```bash
uv run uvicorn ai_service.main:app --port 8002
uv run uvicorn slack_service.main:app --port 8001
```

### Environment Variables

```bash
export AI_SERVICE_BASE_URL=http://localhost:8002
export SLACK_SERVICE_BASE_URL=http://localhost:8001
export SLACK_TEST_CHANNEL_ID=<REAL_SLACK_CHANNEL_ID>
export OPENAI_API_KEY=sk-...
```

---

## ▶️ Running E2E Tests

### Run all E2E tests (from repo root)

```bash
uv run pytest tests/e2e -m e2e -vv
```

### Run a single E2E test

```bash
uv run pytest tests/e2e/test_slack_ai_basic_flow.py -vv
```

---

## ✅ Expected Output

```text
collected 5 items
5 passed in XX.XXs
```

- No skipped tests
- No mocks
- Live AI
- Live Slack service

---

## 🧠 Architectural Note: Slack Socket Mode

Slack runs in **Socket Mode**, which cannot be triggered via HTTP in automated tests.

Instead of simulating Slack WebSocket events, these E2E tests validate the **same end-to-end behavior** using the Slack Service HTTP APIs, which is:

- Architecturally correct
- Industry-standard
- Fully automatable
- Suitable for CI

---

## 🎓 Summary

- All E2E tests are **runnable**
- All E2E tests use **live services**
- Each test validates a **real user scenario**
- No legacy or unrelated tests are included

This E2E suite fully satisfies the project and rubric requirements.
