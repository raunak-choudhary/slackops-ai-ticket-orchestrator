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
