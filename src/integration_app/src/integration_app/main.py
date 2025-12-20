from __future__ import annotations

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from integration_app.config import load_config
from integration_app.slack_entry import SlackEventHandler
from slack_adapter.slack_adapter import SlackServiceClient
from ai_adapter.ai_adapter import register as register_ai_adapter
import jira_adapter  # noqa: F401

register_ai_adapter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HW3 Integration App")


@app.on_event("startup")
def startup() -> None:
    load_config()
    logger.info("Integration app startup complete")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/slack/events")
async def slack_events(request: Request) -> JSONResponse:
    payload = await request.json()

    if payload.get("type") == "url_verification":
        return JSONResponse(
            status_code=200,
            content={"challenge": payload["challenge"]},
        )

    slack_client = SlackServiceClient()
    handler = SlackEventHandler(slack_client)
    result = handler.handle_event(payload)

    return JSONResponse(status_code=200, content=result)
