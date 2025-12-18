from typing import Any


class SlackEventHandler:
    """
    Handles Slack events.

    NOTE:
    This class is intentionally synchronous.
    It is executed inside a FastAPI threadpool.
    """

    def __init__(self) -> None:
        self._slack = None

    def _get_slack(self):
        if self._slack is None:
            # Lazy import to avoid blocking FastAPI startup
            from slack_adapter.slack_adapter import SlackServiceClient
            self._slack = SlackServiceClient()
        return self._slack

    def handle_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        event = payload.get("event", {})

        # Must be a message event
        if event.get("type") != "message":
            return {"status": "ignored"}

        # Ignore bot messages
        if event.get("bot_id"):
            return {"status": "ignored"}

        # Ignore message edits, joins, etc.
        if event.get("subtype"):
            return {"status": "ignored"}

        channel_id = event.get("channel")

        # Slack may put text in different places
        text = event.get("text") or event.get("message", {}).get("text")

        # DEBUG (keep these)
        print("EVENT CHANNEL ID:", channel_id)
        print("EVENT TEXT:", text)

        if not channel_id or not text:
            return {"status": "invalid_event"}

        slack = self._get_slack()
        slack.send_message(
            channel_id=channel_id,
            content="HEY!! Slack event received. Integration app is live.",
        )

        return {"status": "ok"}
