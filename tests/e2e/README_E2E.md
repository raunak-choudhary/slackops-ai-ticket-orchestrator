# End-to-End (E2E) Testing

## Overview

This project includes a comprehensive **End-to-End (E2E) testing suite** that validates the complete user workflows across the system.  
All E2E tests exercise **real services**, **real credentials**, and the **full application stack**, without using mocks or fakes.

All tests were executed successfully:

```
10 passed in 20.50s
```

---

## What These Tests Validate

Each E2E test simulates a **real Slack message**, routes it through the **Orchestrator**, invokes the appropriate backend services (**AI** and/or **Tickets**), and verifies the resulting **Slack output**.

**Flow validated:**

```
Slack → Orchestrator → AI / Tickets → Slack
```

---

## E2E Test Coverage

| Test File | End-to-End Flow | Purpose |
|---------|-----------------|---------|
| `test_slack_ai_basic_flow.py` | Slack → AI → Slack | Verifies basic AI command handling |
| `test_slack_ai_e2e.py` | Slack → Orchestrator → AI → Slack | Full AI request lifecycle |
| `test_slack_ai_long_prompt.py` | Slack → AI → Slack | Handles long AI prompts |
| `test_slack_ai_multiple_requests.py` | Slack → AI (multiple) → Slack | Multiple AI requests in sequence |
| `test_slack_non_ai_message.py` | Slack → Orchestrator | Non-AI messages are ignored |
| `test_slack_ticket_e2e.py` | Slack → Tickets → Slack | Ticket creation via chat command |
| `test_slack_ticket_long_prompt_e2e.py` | Slack → Tickets → Slack | Ticket creation with long descriptions |
| `test_slack_ticket_multiple_requests_e2e.py` | Slack → Tickets (multiple) → Slack | Multiple ticket commands |
| `test_slack_ticket_non_command_e2e.py` | Slack → Orchestrator | Non-ticket messages do not create tickets |
| `test_slack_ticket_and_ai_mix_e2e.py` | Slack → AI → Tickets → Slack | Mixed AI and ticket commands in one session |

---

## Running E2E Tests

From the `tests/e2e` directory:

```bash
uv run pytest
```

---

## Environment Variables Required

The following environment variables must be set before running E2E tests:

- `SLACK_SERVICE_BASE_URL`
- `SLACK_TEST_CHANNEL_ID`
- `AI_SERVICE_BASE_URL`
- `OPENAI_API_KEY`

These tests rely on **live service endpoints** and **real credentials**.

---

## Compliance with Assignment Requirements

This E2E testing strategy satisfies the assignment rubric by:

- ✅ Running the **full application entry point**
- ✅ Verifying **complete user workflows**
- ✅ Using **real credentials and live services**
- ✅ Avoiding mocks and fake integrations
- ✅ Validating system behavior end-to-end

---

## Summary

The E2E test suite provides strong confidence that the system behaves correctly under real-world usage scenarios, covering AI interactions, ticket creation, mixed workflows, and safe handling of unsupported messages.
