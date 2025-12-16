"""Slack client implementation of the ChatInterface protocol."""

from __future__ import annotations

from typing import Optional

import httpx

from chat_api import ChatInterface, Message


class SlackMessage(Message):
    """Slack implementation of the Message abstraction."""

    def __init__(self, message_id: str, content: str, sender_id: str) -> None:
        self._id = message_id
        self._content = content
        self._sender_id = sender_id

    @property
    def id(self) -> str:
        """Unique identifier for the message."""
        return self._id

    @property
    def content(self) -> str:
        """Text content of the message."""
        return self._content

    @property
    def sender_id(self) -> str:
        """Identifier of the message sender."""
        return self._sender_id


def sanitize_text(text: str, max_len: int = 1000) -> str:
    """Normalize message content before sending to Slack."""
    if not isinstance(text, str):
        text = str(text)

    cleaned = "".join(
        ch for ch in text if ch.isprintable() or ch in ("\t", "\n", "\r", " ")
    )
    cleaned = " ".join(cleaned.split())
    return cleaned[:max_len]


class SlackClient(ChatInterface):
    """Slack implementation of the ChatInterface protocol."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        http: Optional[httpx.Client] = None,
    ) -> None:
        self._offline = not (base_url and token)
        self._base_url = (base_url or "").rstrip("/")
        self._token = token or ""
        self._http = http

        if not self._offline:
            self._http = self._http or httpx.Client(
                base_url=self._base_url,
                headers={"Authorization": f"Bearer {self._token}"},
            )

    def send_message(self, channel_id: str, content: str) -> bool:
        """Send a message to a Slack channel."""
        text = sanitize_text(content)

        if self._offline:
            return True

        try:
            assert self._http is not None
            resp = self._http.post(
                "/chat.postMessage",
                json={"channel": channel_id, "text": text},
            )
            resp.raise_for_status()
            return True

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (401, 403):
                raise RuntimeError(
                    "Slack authentication failed while sending message"
                ) from exc
            raise ConnectionError(
                f"Slack API error while sending message: {exc}"
            ) from exc

        except Exception as exc:
            raise ConnectionError(
                f"Failed to send Slack message: {exc}"
            ) from exc

    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]:
        """Retrieve recent messages from a Slack channel."""
        if limit <= 0:
            return []

        if self._offline:
            return [
                SlackMessage("msg-1", "hello", "U001"),
                SlackMessage("msg-2", "world", "U002"),
            ][:limit]

        messages: list[Message] = []
        cursor: Optional[str] = None

        try:
            assert self._http is not None

            while True:
                params = {"channel": channel_id, "limit": limit}
                if cursor:
                    params["cursor"] = cursor

                resp = self._http.get("/conversations.history", params=params)
                resp.raise_for_status()
                data = resp.json()

                for raw in data.get("messages", []):
                    messages.append(
                        SlackMessage(
                            message_id=str(
                                raw.get("client_msg_id")
                                or raw.get("ts")
                                or ""
                            ),
                            content=str(raw.get("text", "")),
                            sender_id=str(raw.get("user", "unknown")),
                        )
                    )
                    if len(messages) >= limit:
                        return messages

                cursor = (
                    data.get("response_metadata", {}).get("next_cursor")
                )
                if not cursor:
                    break

            return messages

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (401, 403):
                raise RuntimeError(
                    "Slack authentication failed while reading messages"
                ) from exc
            raise ConnectionError(
                f"Slack API error while reading messages: {exc}"
            ) from exc

        except Exception as exc:
            raise ConnectionError(
                f"Failed to retrieve Slack messages: {exc}"
            ) from exc

    def delete_message(self, channel_id: str, message_id: str) -> bool:
        """Delete a message from a Slack channel."""
        if self._offline:
            return True

        try:
            assert self._http is not None
            resp = self._http.post(
                "/chat.delete",
                json={"channel": channel_id, "ts": message_id},
            )
            resp.raise_for_status()
            return True

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (401, 403):
                raise RuntimeError(
                    "Slack authentication failed while deleting message"
                ) from exc
            raise ConnectionError(
                f"Slack API error while deleting message: {exc}"
            ) from exc

        except Exception as exc:
            raise ConnectionError(
                f"Failed to delete Slack message: {exc}"
            ) from exc

    def get_channel_members(self, channel_id: str) -> list[str]:
        """Return members of a Slack channel.

        This is a Slack-specific extension used by slack_service.
        """
        if self._offline:
            return ["U001", "U002"]

        try:
            assert self._http is not None
            resp = self._http.get(
                "/conversations.members",
                params={"channel": channel_id},
            )
            resp.raise_for_status()
            data = resp.json()
            return list(data.get("members", []))

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (401, 403):
                raise RuntimeError(
                    "Slack authentication failed while listing members"
                ) from exc
            raise ConnectionError(
                f"Slack API error while listing members: {exc}"
            ) from exc

        except Exception as exc:
            raise ConnectionError(
                f"Failed to retrieve Slack channel members: {exc}"
            ) from exc
