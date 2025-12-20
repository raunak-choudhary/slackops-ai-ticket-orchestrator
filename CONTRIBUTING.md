# Project Overview

This repository represents a product-scale, open-source system designed to integrate multiple independent services into a single, cohesive application. Contributions are encouraged, but they must follow the architectural, design, and development practices outlined in this document to ensure long-term maintainability, consistency, and reliability.

This guide explains how the project is structured, the principles that govern its design, how to get started locally, how testing and continuous integration work, and how to troubleshoot common issues. It is intended to be the primary reference for anyone contributing code, tests, documentation, or infrastructure changes.

---

## Project Architecture

The project is built as a modular, multi-service system composed of three primary verticals: Chat, AI, and Ticketing. Each vertical is developed independently but integrates seamlessly through shared, standardized interfaces.

User input originates from a chat interface and is passed to an AI service for intent detection and reasoning. The AI service produces structured outputs that are executed against a ticketing system using a standardized ticket interface. The results of these operations are then routed back through the chat service and presented to the user.

This architecture allows providers to be swapped without changing core application logic, as long as they adhere to the defined interfaces.

---

## Design Principles

The project follows an interface-first approach using Abstract Base Classes as contracts. Dependency injection is used to decouple business logic from concrete implementations. Provider-specific details are isolated and never leak into shared layers. Testability, observability, and production readiness are treated as first-class concerns.

---

## Repository Layout

All application code lives under the src directory. Interface definitions live in API packages. Provider implementations live in *_impl packages. Orchestration and business logic live in service or integration layers. Tests are organized under the tests directory by scope: unit, integration, and end-to-end.

---

## Development Workflow

All work should be done on feature, fix, or refactor branches created from main. Commits should be small, descriptive, and focused. Before opening a pull request, contributors must ensure all tests, linting, and type checks pass locally.

---

## Getting Started Locally

Clone the repository, install dependencies using uv, activate the virtual environment, and run quality checks. Verify setup by running the application locally.

---

## Testing Strategy

Unit tests validate components in isolation. Integration tests verify interactions without calling live external services. End-to-end tests exercise the full user flow. External APIs must only be accessed via explicitly configured environment variables.

---

## Continuous Integration

Every pull request is validated by CI. The pipeline installs dependencies, runs linting, enforces strict typing, and executes the full test suite. Pull requests will not be merged unless all checks pass.

---

## Pull Request Guidelines

Pull requests should clearly describe what changed, why it was necessary, and how it was tested. Documentation and tests should be updated alongside code changes when applicable.

---

## Troubleshooting

Most issues are caused by missing dependencies, misconfigured environment variables, or interface mismatches. Re-running setup steps and reviewing recent changes typically resolves problems.

---

## Frequently Asked Questions

New providers can be added by implementing the standardized interfaces. Shared interfaces should not be modified without strong justification. Environment variables are required for all external integrations.

---

## Code of Conduct

All contributors are expected to collaborate respectfully and follow professional software engineering standards.
