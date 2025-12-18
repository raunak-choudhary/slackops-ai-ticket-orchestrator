"""
Slack event entrypoint.

Receives Slack events and routes them through the
integration orchestrator.
"""

from __future__ import annotations

import logging
import threading

from integration_app.orchestrator import Orchestrator
from slack_adapter.slack_adapter import SlackServiceClient

logger = logging.getLogger(__name__)


class SlackEventHandler:
    """Handles incoming Slack events."""

    def __init__(self, slack_client: SlackServiceClient) -> None:
        self._slack = slack_client
        self._orchestrator = Orchestrator()

    def handle_event(self, payload: dict) -> dict:
        """Process a Slack event payload and ACK immediately."""
        event = payload.get("event", {})

        # Ignore non-message events
        if event.get("type") != "message":
            return {"status": "ignored"}

        # Ignore bot messages to prevent loops
        if event.get("subtype") == "bot_message":
            return {"status": "ignored"}

        text = (event.get("text") or "").strip()
        channel = event.get("channel")

        logger.info("Slack message received")

        normalized_text = text.lower()

        # AI invocation detection (KNOWN WORKING LOGIC)
        if normalized_text.startswith("/ai") or " ai " in normalized_text:
            logger.info("AI command detected in Slack message")

            threading.Thread(
                target=self._handle_ai_async,
                args=(text, channel),
                daemon=True,
            ).start()

            return {"status": "accepted"}

        logger.debug("Non-AI Slack message ignored")
        return {"status": "ignored"}

    def _handle_ai_async(self, text: str, channel: str) -> None:
        """Handle AI work asynchronously after Slack ACK."""
        try:
            cleaned_text = text

            # Remove Slack mention if present
            if ">" in cleaned_text:
                cleaned_text = cleaned_text.split(">", 1)[1]

            ai_input = (
                cleaned_text
                .replace("/ai", "", 1)
                .replace("ai", "", 1)
                .strip()
            )

            if not ai_input:
                self._slack.send_message(
                    channel,
                    (
                        "AI Assistant\n"
                        "Please provide a prompt after 'ai'.\n\n"
                        "Examples:\n"
                        "/ai Summarize this error\n"
                        "@team4bot ai Explain this in simple terms"
                    ),
                )
                return

            response = self._orchestrator.handle_ai_message(ai_input)

            self._slack.send_message(
                channel,
                f"AI Response:\n{response}",
            )

        except Exception:
            logger.exception("Async AI handling failed")
            self._slack.send_message(
                channel,
                "An error occurred while processing your request.",
            )
