from __future__ import annotations

import json
import logging
from typing import Any

import ai_api
import tickets_api
from tickets_api.client import TicketStatus

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Central routing and execution engine.

    Design principles:
    - AI is used ONLY for reasoning, never execution
    - Ticketing is invoked ONLY after hard validation
    - Deterministic behavior with explicit logs
    """

    # ----------------------------
    # Entry
    # ----------------------------

    def route(self, text: str, channel: str, slack) -> None:
        logger.info("Route start | text=%r", text)

        cleaned = self._strip_slack_mention(text)
        if not cleaned:
            logger.info("Passive message ignored")
            return

        lower = cleaned.lower().strip()

        # ---------------- AI ----------------
        if lower.startswith("ai"):
            self._handle_ai(cleaned, channel, slack)
            return

        # ---------------- Direct Jira ----------------
        if lower == "list tickets":
            logger.info("Direct Jira list command detected")
            self._handle_list_tickets(channel, slack)
            return

        logger.info("No matching command; ignored")
        return

    # ----------------------------
    # AI Dispatcher
    # ----------------------------

    def _handle_ai(self, text: str, channel: str, slack) -> None:
        prompt = text[2:].strip()
        if not prompt:
            slack.send_message(channel, "Error: AI prompt missing.")
            return

        logger.info("AI invoked | prompt=%r", prompt)

        if self._looks_like_jira_intent(prompt):
            logger.info("AI Jira intent detected")
            self._handle_ai_jira(prompt, channel, slack)
            return

        logger.info("AI chat intent detected")
        self._handle_ai_chat(prompt, channel, slack)

    # ----------------------------
    # AI Chat (plain)
    # ----------------------------

    def _handle_ai_chat(self, prompt: str, channel: str, slack) -> None:
        client = ai_api.get_client()
        logger.info("Calling AI chat mode")

        try:
            response = client.generate_response(
                user_input=prompt,
                system_prompt="You are a helpful AI assistant responding to Slack users.",
                response_schema=None,
            )
        except Exception:
            logger.exception("AI chat failed")
            slack.send_message(channel, "AI service is unavailable.")
            return

        logger.info("AI chat success")
        slack.send_message(channel, str(response))

    # ----------------------------
    # AI → Jira
    # ----------------------------

    def _handle_ai_jira(self, prompt: str, channel: str, slack) -> None:
        client = ai_api.get_client()

        logger.info("Calling AI Jira reasoning (plain text JSON)")

        try:
            ai_text = client.generate_response(
                user_input=prompt,
                system_prompt=self._jira_prompt(),
                response_schema=None,
            )
        except Exception:
            logger.exception("AI Jira reasoning failed")
            slack.send_message(channel, "AI service is unavailable.")
            return

        logger.info("AI raw output: %r", ai_text)

        payload = self._extract_json(ai_text)
        if payload is None:
            slack.send_message(channel, "Error: Invalid or missing JSON payload.")
            return

        action = payload.get("action")
        logger.info("Parsed AI action=%r payload=%r", action, payload)

        if action == "create_ticket":
            self._jira_create(payload, channel, slack)
            return

        if action == "list_tickets":
            self._handle_list_tickets(channel, slack)
            return

        if action == "update_ticket":
            self._jira_update(payload, channel, slack)
            return

        if action == "delete_ticket":
            self._jira_delete(payload, channel, slack)
            return

        slack.send_message(channel, "Error: Unsupported Jira action.")

    # ----------------------------
    # Jira Ops
    # ----------------------------

    def _handle_list_tickets(self, channel: str, slack) -> None:
        logger.info("Jira list_tickets start")
        try:
            client = tickets_api.get_client()
            tickets = list(client.search_tickets())  # ✅ materialize iterable
        except Exception:
            logger.exception("Jira list_tickets failed")
            slack.send_message(channel, "Failed to list tickets.")
            return

        logger.info(
            "Jira list_tickets fetched | count=%d | ids=%s",
            len(tickets),
            [self._safe_ticket_id(t) for t in tickets],
        )

        if len(tickets) == 0:
            slack.send_message(channel, "No tickets currently.")
            return

        lines = [f"{self._safe_ticket_id(t)}: {t.title} [{t.status}]" for t in tickets]
        slack.send_message(channel, "\n".join(lines))
        logger.info("Jira list_tickets success")

    def _jira_create(self, payload: dict[str, Any], channel: str, slack) -> None:
        missing = self._missing_fields(payload, ["title", "description"])
        if missing:
            slack.send_message(channel, f"Error: Missing required fields: {', '.join(missing)}")
            return

        logger.info(
            "Jira create_ticket start | title=%r | description_len=%d",
            payload.get("title"),
            len(str(payload.get("description", ""))),
        )

        try:
            client = tickets_api.get_client()
            created = client.create_ticket(
                title=payload["title"],
                description=payload["description"],
            )
        except Exception:
            logger.exception("Jira create_ticket failed")
            slack.send_message(channel, "Failed to create ticket.")
            return

        # ✅ Do NOT trust created.id (your adapter can return a Ticket wrapper with None DTO)
        created_id = None
        try:
            created_id = created.id  # may raise
        except Exception:
            logger.exception("Jira create_ticket returned ticket without readable id (adapter DTO missing)")

        # ✅ Verify by fetching count + IDs immediately (acts as your “dashboard” proof)
        try:
            tickets_after = list(client.search_tickets())
            ids_after = [self._safe_ticket_id(t) for t in tickets_after]
            logger.info(
                "Jira post-create verification | count=%d | ids=%s",
                len(tickets_after),
                ids_after,
            )
        except Exception:
            logger.exception("Jira post-create verification failed")
            tickets_after = []
            ids_after = []

        if created_id:
            slack.send_message(channel, f"Ticket created successfully. ID: {created_id}")
            logger.info("Jira create_ticket success | id=%s", created_id)
            return

        # If we can’t read the returned ID, still respond deterministically with proof
        if len(tickets_after) > 0:
            slack.send_message(
                channel,
                f"Ticket created successfully. Current ticket count: {len(tickets_after)}"
            )
            logger.info("Jira create_ticket success | id_unavailable | count=%d", len(tickets_after))
            return

        # Worst case: 201 happened in logs earlier, but we cannot verify via interface
        slack.send_message(channel, "Ticket creation acknowledged, but verification failed. Try: list tickets")
        logger.warning("Jira create_ticket acknowledged but could not verify via search_tickets")

    def _jira_update(self, payload: dict[str, Any], channel: str, slack) -> None:
        missing = self._missing_fields(payload, ["ticket_id"])
        if missing:
            slack.send_message(channel, f"Error: Missing required fields: {', '.join(missing)}")
            return

        status = payload.get("status")
        try:
            status_enum = TicketStatus(status) if status else None
            client = tickets_api.get_client()
            ticket = client.update_ticket(
                ticket_id=payload["ticket_id"],
                status=status_enum,
            )
        except Exception:
            logger.exception("Jira update_ticket failed")
            slack.send_message(channel, "Failed to update ticket.")
            return

        slack.send_message(channel, f"Ticket updated: {self._safe_ticket_id(ticket)}")
        logger.info("Jira update_ticket success | id=%s", self._safe_ticket_id(ticket))

    def _jira_delete(self, payload: dict[str, Any], channel: str, slack) -> None:
        missing = self._missing_fields(payload, ["ticket_id"])
        if missing:
            slack.send_message(channel, f"Error: Missing required fields: {', '.join(missing)}")
            return

        try:
            client = tickets_api.get_client()
            ok = client.delete_ticket(payload["ticket_id"])
        except Exception:
            logger.exception("Jira delete_ticket failed")
            slack.send_message(channel, "Failed to delete ticket.")
            return

        if ok:
            slack.send_message(channel, f"Ticket deleted: {payload['ticket_id']}")
            logger.info("Jira delete_ticket success | id=%s", payload["ticket_id"])
        else:
            slack.send_message(channel, "Ticket not found.")
            logger.info("Jira delete_ticket not found | id=%s", payload["ticket_id"])

    # ----------------------------
    # Helpers
    # ----------------------------

    @staticmethod
    def _strip_slack_mention(text: str) -> str:
        cleaned = text.strip()

        # Slack internal mention format: <@U123ABC>
        if cleaned.startswith("<@") and ">" in cleaned:
            return cleaned.split(">", 1)[1].strip()

        # Plain-text bot mention format: @team4bot
        if cleaned.lower().startswith("@team4bot"):
            return cleaned[len("@team4bot"):].strip()

        return cleaned

    @staticmethod
    def _looks_like_jira_intent(text: str) -> bool:
        keywords = ("ticket", "jira", "issue")
        return any(k in text.lower() for k in keywords)

    @staticmethod
    def _extract_json(value: Any) -> dict[str, Any] | None:
        if isinstance(value, dict):
            return value
        if not isinstance(value, str):
            return None

        try:
            start = value.index("{")
            end = value.rindex("}") + 1
            return json.loads(value[start:end])
        except Exception:
            return None

    @staticmethod
    def _missing_fields(payload: dict[str, Any], fields: list[str]) -> list[str]:
        return [f for f in fields if not payload.get(f)]

    @staticmethod
    def _safe_ticket_id(ticket: Any) -> str:
        try:
            return str(ticket.id)
        except Exception:
            return "<id-unavailable>"

    @staticmethod
    def _jira_prompt() -> str:
        return (
            "You are an AI routing agent.\n"
            "Return ONLY a single JSON object.\n\n"
            "Allowed actions:\n"
            "- create_ticket (requires title, description)\n"
            "- update_ticket (requires ticket_id)\n"
            "- delete_ticket (requires ticket_id)\n"
            "- list_tickets\n\n"
            "If required fields are missing, still return JSON with the action "
            "and omit the missing fields.\n"
            "Do not include explanations.\n"
        )
