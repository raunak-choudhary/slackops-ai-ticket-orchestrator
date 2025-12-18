"""
Main entry point for the HW3 integration application.

This service:
- Activates dependency injection for AI and Slack adapters
- Exposes the Slack Events API endpoint
- Coordinates cross-vertical integration logic
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from integration_app.config import load_config
from integration_app.slack_entry import SlackEventHandler
from slack_adapter.slack_adapter import SlackServiceClient

# -------------------------
# CRITICAL: Activate AI DI
# -------------------------
from ai_adapter.ai_adapter import register as register_ai_adapter

register_ai_adapter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HW3 Integration App")


@app.on_event("startup")
def startup() -> None:
    """Application startup hook."""
    load_config()
    logger.info("Integration app startup complete")


@app.post("/slack/events")
async def slack_events(request: Request) -> JSONResponse:
    """Slack Events API endpoint."""
    payload = await request.json()

    # Slack URL verification handshake
    if payload.get("type") == "url_verification":
        return JSONResponse(
            status_code=200,
            content={"challenge": payload["challenge"]},
        )

    slack_client = SlackServiceClient()
    handler = SlackEventHandler(slack_client)

    result = handler.handle_event(payload)
    return JSONResponse(status_code=200, content=result)
