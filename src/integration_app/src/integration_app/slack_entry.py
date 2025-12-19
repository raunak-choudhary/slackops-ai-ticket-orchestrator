# integration_app/slack_entry.py

from __future__ import annotations

import logging
import threading

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

logger = logging.getLogger(__name__)


class SlackEventHandler:
    def __init__(self, slack_client: SlackServiceClient) -> None:
        self._slack = slack_client
        self._orchestrator = Orchestrator()

    def handle_event(self, payload: dict) -> dict:
        event = payload.get("event", {})

        if event.get("type") != "message":
            return {"status": "ignored"}

        if event.get("bot_id") is not None:
            return {"status": "ignored"}

        text = (event.get("text") or "").strip()
        channel = event.get("channel")

        threading.Thread(
            target=self._orchestrator.route,
            args=(text, channel, self._slack),
            daemon=True,
        ).start()

        return {"status": "accepted"}
