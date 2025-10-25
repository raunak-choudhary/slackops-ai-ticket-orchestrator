# Slack API Package

This package defines the **abstract contract** for the Slack Chat service.  
It provides type-safe definitions for the following interfaces:

- `Channel`, `Message`, and `User` data models  
- `TokenStore` protocol for managing OAuth tokens  
- `ChatClient` abstract base class defining the core chat operations  
  (`list_channels`, `list_messages`, `send_message`, `delete_message`)

These interfaces are used by:
- `slack_impl` for the concrete API integration with Slack
- `slack_service` for exposing the API via FastAPI endpoints
- `slack_adapter` (later) to wrap the generated client for location transparency

**Note:** This package should not depend on any external SDKs or Slack libraries.
