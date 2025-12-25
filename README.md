# SlackOps: AI Ticket Orchestrator

**SlackOps: AI Ticket Orchestrator** is a Slack-first automation platform that transforms natural-language requests into structured AI-driven decisions and executes them reliably against ticketing systems. The system routes chat input through an AI reasoning layer, validates and performs ticket operations via standardized interfaces, and responds back in Slack—demonstrating production-grade orchestration, testing, observability, and infrastructure practices. This project was built following the engineering guidelines of the **Open Source and Professional Software Development (OSPSD)** course, with a strong emphasis on modular design, correctness, and operational readiness.

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

---

## Repository Layout

```
.
├── src/
│   ├── chat_api/
│   ├── ai_api/
│   ├── tickets_api/
│   ├── *_impl/
│   ├── *_adapter/
│   ├── *_service/
│   └── integration_app/
├── tests/
├── .circleci/
├── pyproject.toml
├── README.md
├── DESIGN.md
├── COMPONENT.md
└── CONTRIBUTING.md
```

---

## Prerequisites

- Python 3.11+
- uv
- git
- Provider credentials (Slack, AI, ticket system)

---

## Running the System Locally

Use either the integrated entrypoint or run components individually for debugging.

Integrated run:

```bash
python main.py
```

Or via Uvicorn:

```bash
PYTHONPATH=src uv run uvicorn integration_app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Testing

```bash
pytest
pytest tests/integration
pytest tests/e2e
```

---

## Documentation Index

- README.md
- DESIGN.md
- COMPONENT.md
- CONTRIBUTING.md
