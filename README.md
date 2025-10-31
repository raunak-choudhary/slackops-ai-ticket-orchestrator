# Slack Service Package

This package exposes the **Slack Chat API** as a **FastAPI microservice**.

It imports the concrete implementation from `slack_impl` and provides
network-accessible endpoints for:

- `GET /channels` — list all channels
- `GET /channels/{id}/messages` — retrieve messages in a channel
- `POST /channels/{id}/messages` — send a new message
- `DELETE /channels/{id}/messages/{ts}` — delete a message (optional)

Additional Features:
- `/health` endpoint for CircleCI and Render deployment verification
- OAuth 2.0 authentication flow endpoints
- SQLite token store integration for local development

**Deployment:**  
This service is deployed via Render with automatic build triggers from CircleCI.
Environment variables (`SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, etc.) are managed securely.
---

# HW2 - Slack API Chat Service

## Overview
For Homework 2, our team extended the OSPD architecture to design and deploy a **Slack Chat Service** following the same modular structure as in HW1 — consisting of API, Implementation, FastAPI Service, and Adapter layers. This microservice wraps the official Slack API, exposing endpoints for channels, messages, and authentication via OAuth 2.0.

The system achieves **location transparency** through Dependency Injection (DI) across all layers, enabling seamless swapping between local and remote implementations.

## Core Modules

### 1. slack_api
- Defines the abstract interface for Slack operations (channels, messages, users).
- Independent of external Slack SDKs — pure contract definitions.
- Includes data validation and schema consistency tests.

### 2. slack_impl
- Implements the `slack_api` interface.
- Integrates with the **Slack Web API** and implements a complete **OAuth 2.0 authentication flow**.
- OAuth tokens are securely stored in a **SQLite database** using a lightweight token store (`token_store.py`).
- The `slack_client.py` module wraps all core Slack API operations, including:
  - Listing channels
  - Fetching messages
  - Posting messages with sanitization
  - Health checks and offline fallbacks

### 3. slack_service
- Built using **FastAPI**, providing network-accessible endpoints:
  - `GET /channels` — list all available Slack channels.
  - `GET /channels/{id}/messages` — retrieve messages for a given channel.
  - `POST /channels/{id}/messages` — send a new message to a Slack channel.
  - `/health` — operational check for Render and CircleCI builds.
  - `/auth` and `/callback` — handle OAuth 2.0 flow (user authorization and token exchange).
- Deployed publicly on Render at:  
  **[https://ospsd-hw2-final-demo.onrender.com/docs](https://ospsd-hw2-final-demo.onrender.com/docs)**

### 4. slack_adapter
- Wraps the auto-generated OpenAPI client for the deployed Slack service.
- Implements the same interface as `slack_api`, providing transparent remote usage.
- Enables `main.py` to switch between local (impl) and remote (adapter) modes via DI.

## Testing and Coverage
Comprehensive testing was performed across unit, integration, and service layers.  
Command used:
```bash
uv run pytest -q --cov=src --cov-report=xml --junitxml=test-results/junit.xml
```
**Results:**
- Total tests executed: 69 (with 2 email-related tests skipped)
- Total coverage: **90.06%**
- Coverage threshold (85%) successfully met.
- Slack tests include:
  - `src/slack_api/tests/` → Contract & Type Validation Tests
  - `src/slack_impl/tests/` → OAuth, Token Store, Health, Channel, and Post Message tests
  - `src/slack_service/tests/` → FastAPI Endpoint Tests
  - `src/slack_adapter/tests/` → Integration & Adapter Contract Tests

## CI/CD Pipeline (CircleCI)
A fully automated **9-job CircleCI pipeline** ensures reliability and maintainability.  
Each job passes successfully (9/9 green checks).

**Pipeline Jobs:**
1. `precheck` — initial environment setup
2. `ruff_lint` — style and formatting check using Ruff
3. `mypy_strict_checks` — strict type checking for all Slack packages
4. `pytest_coverage` — unit and integration tests with 85%+ coverage enforcement
5. `build` — packaging and dependency validation via `uv`
6. `report_summary` — collect test artifacts and coverage XML
7. `deployment_health_check` — validates `/health` endpoint returns 200 OK post-deploy
8. `circleci_test` — consolidated CI sanity check
9. `auto_deploy_render` — triggers automatic deployment to Render

## Deployment (Render)
The service is deployed on Render with the following configuration:
- **Platform:** Render Web Service (Python 3.12.12 + uv)
- **URL:** [https://ospsd-hw2-final-demo.onrender.com/docs](https://ospsd-hw2-final-demo.onrender.com/docs)
- **Environment Variables:** managed via Render Secrets (e.g., `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`)
- **Database:** Local SQLite initialized via `scripts/sqlite_init.sql`
- **Health Endpoint:** `/health` returns 200 OK

## Dependency Injection (DI) Validation
Each Slack component was verified for correct DI linkage:
- `slack_api` ↔ `slack_impl` ↔ `slack_service` ↔ `slack_adapter`
- The same contract class can be injected into `main.py` for both local (impl) and remote (adapter) modes.
- DI verification confirmed **green** across all modules.

## Summary
✅ Slack Chat Service implemented and deployed successfully.  
✅ OAuth 2.0 integrated with secure SQLite token management.  
✅ Ruff, MyPy strict, and Pytest (90.06% coverage) passed.  
✅ 9/9 CircleCI jobs successful.  
✅ Public deployment verified on Render with operational `/health` endpoint.