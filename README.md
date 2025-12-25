# SlackOps: AI Ticket Orchestrator

**SlackOps: AI Ticket Orchestrator** is a Slack-first automation platform that transforms natural-language requests into structured AI-driven decisions and executes them reliably against ticketing systems. The system routes chat input through an AI reasoning layer, validates and performs ticket operations via standardized interfaces, and responds back in Slack, demonstrating production-grade orchestration, testing, observability, and infrastructure practices. This project was built following the engineering guidelines of the **Open Source and Professional Software Development (OSPSD)** course, with a strong emphasis on modular design, correctness, and operational readiness.

This repository contains a **provider-agnostic, interface-driven system** that connects a **Chat** interface to an **AI reasoning layer** and a **Ticketing system**. The goal is simple:

> A user types a natural-language request in chat (e.g., “Create a ticket for fixing the login bug”).  
> The system routes the text to AI, the AI returns a structured action, the Ticketing layer executes it, and Chat replies with the result.

If you follow this README step-by-step, you should be able to **set up the project locally**, **run the full stack**, and **run unit / integration / end-to-end tests**.

---

## Table of Contents

1. [Quick Start (Fastest Path)](#quick-start-fastest-path)  
2. [Project Philosophy](#project-philosophy)  
3. [Quickstart Component Stack](#quickstart-component-stack)  
4. [How the System Works](#how-the-system-works)  
5. [Repository Layout](#repository-layout)  
6. [Prerequisites](#prerequisites)  
7. [Project Setup (Detailed)](#project-setup-detailed)  
8. [Configuration & Environment Variables](#configuration--environment-variables)  
9. [Running the System Locally](#running-the-system-locally)  
10. [Testing](#testing)  
11. [Infrastructure & Deployment Notes](#infrastructure--deployment-notes)  
12. [Continuous Integration](#continuous-integration)  
13. [Development Workflow](#development-workflow)  
14. [Troubleshooting](#troubleshooting)  
15. [Documentation Index](#documentation-index)

---

## Quick Start (Fastest Path)

This is the minimum you should do to verify you can run the repository locally.

### 1) Clone and enter the repo

```bash
git clone https://github.com/raunak-choudhary/slackops-ai-ticket-orchestrator.git
cd slackops-ai-ticket-orchestrator
```

### 2) Install dependencies (workspace)

This project uses `uv` for dependency management.

```bash
uv sync --all-packages --dev
```

### 3) Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4) Set required environment variables

Create a `.env` file (recommended) **or** export them in your shell.

```bash
# Example (do NOT commit real keys)
export OPENAI_API_KEY="..."
export SLACK_BOT_TOKEN="..."
```

(See [Configuration & Environment Variables](#configuration--environment-variables) for the full list.)

### 5) Run quality checks

```bash
ruff check .
mypy src tests
pytest
```

### 6) Run the application

```bash
python main.py
```

If the app starts without errors, your environment is set correctly.

---

## Project Philosophy

This repository is built around a few non-negotiable engineering values:

### Interface-first design (ABCs as contracts)

Each vertical (Chat, AI, Ticketing) is defined by a standardized **Abstract Base Class (ABC)** contract. Implementations must strictly conform to these contracts so that provider details never leak into core logic.

### Provider-agnostic implementations

The system is designed so you can swap providers (e.g., different AI providers, different ticket providers) with minimal change, ideally through configuration rather than rewrites.

### Dependency Injection (IoC)

Business logic never instantiates provider implementations directly. Instead, implementations are **injected** (via factories/configuration) so that:
- providers can be swapped,
- tests can use fakes/mocks,
- orchestration stays clean and readable.

### Testability & production readiness

Unit, integration, and end-to-end tests are treated as first-class features. The system is also designed so it can be deployed and monitored in a remote environment.

---

## Quickstart Component Stack

At runtime, the system is composed of these layers:

```
┌──────────────────────────┐
│ Chat Provider / Adapter   │  ← receives user input, sends responses
└─────────────▲────────────┘
              │
┌─────────────┴────────────┐
│ AI Provider / Adapter     │  ← intent + reasoning, returns structured output
└─────────────▲────────────┘
              │
┌─────────────┴────────────┐
│ Ticket Provider / Adapter │  ← executes ticket operations (CRUD/search/update)
└──────────────────────────┘
```

The “Integration App” (or orchestrator) wires these layers together through interfaces.

---

## How the System Works

The system follows a consistent “user flow loop”:

1. **User Input (Chat)**  
   A user sends a natural-language message through a chat interface.

2. **Routing & Reasoning (AI)**  
   The AI layer determines what the user wants (intent), extracts parameters, and returns a structured payload.

3. **Execution (Ticket Service)**  
   The ticket layer receives a structured action (e.g., `create_ticket`) and executes it against the ticket provider.

4. **Response (Chat)**  
   The system formats a response and sends it back to the user through chat.

### Example: “Create a ticket”

User message:

> “Create a ticket for fixing the login bug and assign it to me.”

AI structured output (example shape; actual schema may vary):

```json
{
  "action": "create_ticket",
  "title": "Fix login bug",
  "description": "Login fails under certain session conditions",
  "assignee": "me"
}
```

Ticket layer executes:

```python
ticket = tickets.create_ticket(
    title=payload["title"],
    description=payload["description"],
    assignee=payload.get("assignee"),
)
```

Chat responds:

> “ Ticket created: TICKET-123 — Fix login bug”

---

## Repository Layout

The repository is organized by components/verticals:

```
.
├── src/
│   ├── chat_api/               # Chat interface contracts
│   ├── ai_api/                 # AI interface contracts
│   ├── tickets_api/            # Ticket interface contracts
│   ├── *_impl/                 # Provider-specific implementations (OpenAI, Gemini, Jira, etc.)
│   ├── *_adapter/              # Adaptation layers / clients
│   ├── *_service/              # Service logic (business rules)
│   └── integration_app/        # Wiring + orchestration (entrypoints, DI/config)
│
├── tests/
│   ├── unit/                   # Unit tests (pure logic)
│   ├── integration/            # Integration tests (component-to-component)
│   └── e2e/                    # End-to-end tests (full flow)
│
├── .circleci/                  # CI pipeline definitions
├── pyproject.toml              # Workspace configuration
├── README.md                   # This file
├── DESIGN.md                   # Architecture and design rationale
├── COMPONENT.md                # Component documentation index
└── CONTRIBUTING.md             # Contribution guidelines
```

> Tip: If you're new to the repo, read `COMPONENT.md` first for a guided map of what exists and where.

---

## Prerequisites

You should have:

- **Python** (project targets Python 3.11+; your environment may use 3.12)
- **uv** installed and available in PATH
- `git`
- Optional but helpful: `make` (if your local workflow uses Makefiles)
- Credentials for providers you want to run (Slack bot token, AI keys, ticket provider tokens)

### Verify tools

```bash
python --version
uv --version
git --version
```

---

## Project Setup (Detailed)

This is the step-by-step onboarding flow we expect all contributors to follow.

### 1) Clone the repo

```bash
git clone https://github.com/raunak-choudhary/slackops-ai-ticket-orchestrator.git
cd slackops-ai-ticket-orchestrator
```

### 2) Install dependencies for the full workspace

```bash
uv sync --all-packages --dev
```

If you only want to work on one package, you can still sync the full workspace to avoid resolution issues.

### 3) Activate the environment

```bash
source .venv/bin/activate
```

### 4) Confirm you can run quality checks

```bash
ruff check .
mypy src tests
pytest
```

If any step fails, jump to [Troubleshooting](#troubleshooting).

---

## Configuration & Environment Variables

This project intentionally does **not** hardcode secrets.  
All credentials must be provided via environment variables.

### Recommended: use a `.env` file

Create a `.env` file at the repository root:

```bash
# AI Provider keys
OPENAI_API_KEY="..."
GEMINI_API_KEY="..."

# Chat provider credentials
SLACK_BOT_TOKEN="..."
SLACK_SIGNING_SECRET="..."

# Ticket provider credentials
JIRA_API_TOKEN="..."
JIRA_BASE_URL="..."
JIRA_EMAIL="..."
```

> Do not commit `.env`. Add it to `.gitignore` if it is not already ignored.

### Loading `.env`

Depending on how the app is started, you may load `.env` automatically (if the app uses dotenv) or manually:

```bash
set -a
source .env
set +a
```

### Common failure pattern

If you see an error like:

> Missing required environment variable: OPENAI_API_KEY

That means the app is configured to require that variable at startup.

---

## Running the System Locally

There are two common ways to run the project locally:

1. **Single entrypoint** (recommended): run one command that starts the integrated system.
2. **Component-by-component**: start services independently (useful for debugging).

### Option A: Run the integrated entrypoint

From the repository root:

```bash
python main.py
```

If your integrated app is served via Uvicorn (example):

```bash
PYTHONPATH=src uv run uvicorn integration_app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option B: Run components individually (debugging)

If you are diagnosing an issue, you may run components one-by-one.  
For example, if a service is a FastAPI app, run it with Uvicorn from its package directory.

Example pattern:

```bash
cd src/<component_name>
uv run uvicorn <module_path>:app --port <port>
```

> Use this when you want to isolate a failure (e.g., AI provider vs ticket provider).

---

## Testing

Testing is a core requirement of this repository. Tests are organized by scope.

### 1) Unit Tests

Unit tests validate logic without depending on external services.

Run all tests:

```bash
pytest
```

Run a specific folder:

```bash
pytest tests/unit
```

### 2) Integration Tests

Integration tests validate that two components correctly interact (e.g., orchestrator + ticket service), generally using mocks or fakes for external APIs.

```bash
pytest tests/integration
```

### 3) End-to-End (E2E) Tests

E2E tests validate the full pipeline (Input → Reasoning → Execution → Output).  
They may require real credentials depending on how the repository is configured.

```bash
pytest tests/e2e
```

### Markers and selective runs

If the repo uses pytest markers, use:

```bash
pytest -m "integration"
pytest -m "e2e"
```

If you are uncertain which markers exist, run:

```bash
pytest --markers
```

### Coverage (optional)

```bash
uv run pytest --cov=src --cov-report=term-missing
```

---

## Infrastructure & Deployment Notes

This project is designed to be deployable to a remote environment using Infrastructure as Code (IaC).  
The deployed environment should provide:

- Environment variables for secrets
- Networking for any API endpoints
- Observability/telemetry configuration where applicable

> This README focuses on local development. Deployment details belong in the IaC folder or a dedicated `DEPLOYMENT.md` if your team created one.

---

## Continuous Integration

This repository uses CI to enforce code quality and prevent regressions.

CI typically runs:
- `ruff check .`
- `mypy src tests` (strict typing)
- `pytest` (unit/integration/e2e depending on configuration)

CI should be treated as the “source of truth” for merge readiness.  
If CI fails, fix the underlying issue rather than bypassing checks.

---

## Development Workflow

A clean workflow keeps the repo stable and easy to review.

### Branching

Use branches like:

- `feature/<short-name>` for features
- `fix/<short-name>` for bugs
- `refactor/<short-name>` for cleanups

### Commit messages

Use clear prefixes:

- `feat: ...`
- `fix: ...`
- `test: ...`
- `docs: ...`
- `refactor: ...`

### Pull Requests

A good pull request should include:
- A short summary of what changed
- Why the change was needed
- How it was tested (commands + results)

---

## Troubleshooting

### 1) “uv sync” dependency errors

If `uv sync` fails, ensure:
- You are at the repo root
- You are using the correct Python version
- You ran `uv sync --all-packages --dev`

Try:

```bash
uv sync --all-packages --dev --reinstall
```

### 2) Ruff failures (lint)

Run:

```bash
ruff check . --fix
```

If it still fails, read the error and fix it at the reported file and line.

### 3) Mypy failures (typing)

Mypy failures usually mean:
- Missing type annotations
- Interface mismatch
- Incorrect return types

Run:

```bash
mypy src tests
```

Fix type issues rather than disabling strict mode.

### 4) Missing environment variables

If startup fails with “Missing required environment variable”, export the variable or set it in `.env` and reload.

### 5) E2E tests failing

Common reasons:
- Missing real credentials
- Incorrect chat provider setup
- External provider rate limits

Start by:
- Confirming env vars are set
- Running unit/integration tests first
- Running E2E tests last

---

## Documentation Index

This repository includes multiple docs, each with a specific purpose:

- **README.md**: How to run the system and understand the big picture
- **DESIGN.md**: Architecture, design choices, and system rationale
- **COMPONENT.md**: Component index and responsibilities
- **CONTRIBUTING.md**: Contribution rules, PR process, and repo hygiene

---

## What to Read Next

If you are new:
1. Read `COMPONENT.md` to understand what exists.
2. Read `DESIGN.md` to understand why it’s designed that way.
3. Use this README to run the system and tests.
4. Use `CONTRIBUTING.md` before opening a PR.
