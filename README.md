# OSPSD — Homework 3 (Submission 2) Update
## Standardized Chat + Multi‑AI Integration (Slack, OpenAI, Gemini)

---

## 1. Repository Purpose (Evaluator‑First Overview)

This repository demonstrates **Homework 3 – Submission 2** for the **Open Source Product‑Scale Development (OSPSD)** course.

The primary evaluation target for **Submission‑2** is **AI vertical integration**, verified through **integration tests**.

**What matters for grading:**
- Standardized APIs as the single source of truth
- Clean backend integration (no UI required)
- Real communication with AI providers
- Tests that prove the system works end‑to‑end

No frontend, no hosted deployment, and no real‑time websocket system are required.

---

## 2. Minimal Context from HW2 (Retained for Continuity)

Homework 2 introduced the **Chat vertical**, using **Slack** as the platform.

From HW2, the following components are retained and reused:

- **Standardized Chat API (`chat_api`)**
  - Defines the minimal chat contract:
    - `send_message`
    - `get_messages`
    - `delete_message`
- **Slack implementation stack**
  - `slack_api` – low‑level Slack Web API wrapper
  - `slack_impl` – OAuth, token storage, Slack calls
  - `slack_adapter` – adapter implementing `ChatInterface`
  - `slack_service` – FastAPI service (used internally)

HW2 deployment details (Render, OAuth redirect URLs, etc.) are **not required** for HW3 grading and are intentionally de‑emphasized.

Slack is treated purely as a **chat transport**, not a UI.

---

## 3. HW3 Submission‑2 Focus: AI Vertical Integration

Homework 3 (Submission‑2) builds on the Chat vertical by introducing a **standardized AI vertical**.

### Goals Achieved
- Introduced a **standardized AI API**
- Implemented **multiple AI providers**
- Proved provider‑agnostic routing
- Verified real integrations using tests

The resulting backend flow is:

```
Chat → AI → Chat
```

Slack acts as the interface.  
AI providers are interchangeable.

---

## 4. Architecture Overview

### Chat Vertical
- `chat_api` – standardized chat contract
- `slack_api` – Slack platform client
- `slack_impl` – Slack OAuth & Web API implementation
- `slack_adapter` – implements `ChatInterface`
- `slack_service` – routing & polling logic

### AI Vertical (HW3)
- `ai_api` – standardized AI interface (`AIInterface`)
- `ai_impl`
  - `OpenAIClient`
  - `GeminiClient`

### Integration Layer
- `slack_service/ai_router.py`
  - Polls messages
  - Extracts AI commands
  - Invokes `AIInterface`
  - Sends response back via `ChatInterface`

The router contains **no provider‑specific logic**.

---

## 5. Installation Instructions (For TAs / Evaluators)

### 5.1 Requirements
- Python **3.12+**
- Dependency manager: **uv**

Install `uv` if needed:
```bash
pip install uv
```

### 5.2 Install All Dependencies
From the repository root:
```bash
uv sync
```

This installs all internal packages in editable mode:
- chat_api
- slack_api
- slack_impl
- slack_adapter
- slack_service
- ai_api
- ai_impl

---

## 6. AI SDK Dependencies

Real integration tests require the following SDKs (already included via `uv`):

| Provider | SDK |
|--------|-----|
| OpenAI | `openai` |
| Gemini | `google-generativeai` |

---

## 7. Environment Variables

Create a `.env` file at the repository root:

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
SLACK_CHANNEL_ID=C...
```

**Important notes:**
- Secrets are never committed
- Tests automatically **skip** if keys are missing
- This behavior is intentional and CI‑safe

To export locally:
```bash
export $(grep -v '^#' .env | xargs)
```

---

## 8. HW3 Integration Tests (Primary Grading Artifact)

### 8.1 Run All Tests
```bash
uv run pytest
```

Expected behavior:
- Chat API tests pass
- AI provider tests pass **or skip safely**
- No failures due to missing secrets

---

### 8.2 Chat API Integration Tests
- `test_chat_send_message.py`
- `test_chat_get_messages.py`
- `test_chat_delete_message.py`

Each standardized chat method is tested independently.

---

### 8.3 Real AI Provider Integration Tests

**OpenAI**
```bash
uv run pytest tests/integration/test_openai_real_integration.py
```

**Gemini**
```bash
uv run pytest tests/integration/test_gemini_real_integration.py
```

Both tests:
- Call the provider for real
- Skip automatically if API keys are missing
- Are safe for CI execution

---

### 8.4 Slack → AI → Chat Integration
```bash
uv run pytest tests/integration/test_slack_openai_integration.py
```

This test proves:
- Polling‑based chat retrieval
- AI invocation
- Response routing back to chat

---

### 8.5 AI Provider Substitution Test (Best‑Attempt)
```bash
uv run pytest tests/integration/test_slack_gemini_provider_selection.py
```

This test proves:
- `ai_router` depends only on `AIInterface`
- Gemini can replace OpenAI without router changes

---
## 9. Notes for Evaluators

- Slack is the interaction surface
- Polling is used (explicitly approved by TA)
- No frontend or deployment required
- Integration tests are the authoritative proof

---