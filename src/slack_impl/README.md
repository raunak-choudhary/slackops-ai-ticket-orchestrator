# Slack Implementation Package

This package provides the **concrete implementation** of the Slack Chat service.

It connects the abstract interfaces defined in `slack_api` to the real Slack Web API
via HTTP calls. In development mode, this can be mocked to avoid network dependency.

Responsibilities:
- Implements `ChatClient` methods using the Slack REST endpoints
- Handles OAuth 2.0 token retrieval and storage (via `TokenStore`)
- Translates Slack responses into strongly typed `Message` and `Channel` objects

**Note:** Keep all Slack SDK logic isolated here. The rest of the system should
only depend on the abstract `slack_api` interfaces.
