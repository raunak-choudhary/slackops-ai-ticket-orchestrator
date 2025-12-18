from __future__ import annotations

import logging

import ai_api

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Central routing and execution engine.

    Responsibilities:
    - Deterministic command parsing
    - Explicit verb handling only
    - No Slack SDK usage
    - No business logic in Slack event handler
    """

    def route(self, text: str, channel: str, slack) -> None:
        # Strip Slack mention if present
        cleaned = text
        if ">" in cleaned:
            cleaned = cleaned.split(">", 1)[1]
        cleaned = cleaned.strip()

        if not cleaned:
            return

        lower = cleaned.lower()
        tokens = lower.split()

        # ---------------- AI ----------------
        if lower.startswith("ai"):
            self._handle_ai(cleaned, channel, slack)
            return

        # ---------------- LIST MEMBERS ----------------
        if lower == "list members":
            self._handle_list_members(channel, slack)
            return

        # ---------------- LIST CHANNELS ----------------
        if lower == "list channels":
            self._handle_list_channels(channel, slack)
            return

        # ---------------- DELETE MESSAGE ----------------
        if lower.startswith("delete message"):
            self._handle_delete_message(tokens, channel, slack)
            return

        # ---------------- UNKNOWN COMMAND ----------------
        # Rule:
        # - Single word → ignore (e.g., "hello")
        # - Multi-word → explicit but unsupported command
        if len(tokens) >= 2:
            slack.send_message(channel, "Unknown command.")
            return

        # Otherwise: ignore silently
        return

    # ======================================================
    # Handlers
    # ======================================================

    def _handle_ai(self, text: str, channel: str, slack) -> None:
        prompt = text[2:].strip()

        if not prompt:
            slack.send_message(
                channel,
                "AI Assistant\nPlease provide a prompt after 'ai'."
            )
            return

        client = ai_api.get_client()
        logger.info("Invoking AI service")

        response = client.generate_response(
            user_input=prompt,
            system_prompt="You are a helpful AI assistant responding to Slack users.",
            response_schema=None,
        )

        slack.send_message(channel, f"AI Response:\n{response}")

    def _handle_list_members(self, channel: str, slack) -> None:
        members = slack.get_channel_members(channel)

        if not members:
            slack.send_message(channel, "No members found.")
            return

        slack.send_message(channel, "\n".join(members))

    def _handle_list_channels(self, channel: str, slack) -> None:
        # Placeholder for future expansion
        slack.send_message(channel, "Listing channels is not implemented yet.")

    def _handle_delete_message(self, tokens: list[str], channel: str, slack) -> None:
        if len(tokens) != 3:
            slack.send_message(channel, "Usage: delete message <timestamp>")
            return

        message_id = tokens[2]
        slack.delete_message(channel, message_id)
        slack.send_message(channel, "Message deleted.")
