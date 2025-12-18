"""
Core orchestration logic for the integration application.

This module coordinates calls between Slack, AI, and (future)
Ticketing services while remaining provider-agnostic.
"""

from __future__ import annotations

import logging

import ai_api

logger = logging.getLogger(__name__)


class Orchestrator:
    """Main orchestration engine."""

    def handle_ai_message(self, user_input: str) -> str:
        """
        Handle a Slack message that explicitly invokes AI.

        CURRENT BEHAVIOR:
        - Returns plain-text AI responses (conversational mode).

        FUTURE (HW3 FINAL / EXTRA CREDIT):
        - Pass a response_schema here to enable structured
          tool calls for Slack → AI → Ticket workflows.
        """
        logger.info("Orchestrating AI request")

        client = ai_api.get_client()  # always resolves latest DI binding
        logger.debug("AI client resolved via dependency injection")

        return client.generate_response(
            user_input=user_input,
            system_prompt=(
                "You are a helpful AI assistant responding to Slack users. "
                "Keep responses concise and professional."
            ),
            response_schema=None,
        )
