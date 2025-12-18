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
        return self._id

    @property
    def content(self) -> str:
        return self._content

    @property
    def sender_id(self) -> str:
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
                headers={
                    "Authorization": f"Bearer {self._token}",
                    "Content-Type": "application/json",
                },
            )

    def send_message(self, channel_id: str, content: str) -> bool:
        """Send a message to a Slack channel."""
        text = sanitize_text(content)

        if self._offline:
            print("SLACK OFFLINE MODE — message skipped")
            return True

        payload = {
            "channel": channel_id,
            "text": text,
        }

        print("SLACK POST PAYLOAD:", payload)

        try:
            assert self._http is not None
            resp = self._http.post("/chat.postMessage", json=payload)

            print("SLACK STATUS:", resp.status_code)
            print("SLACK RESPONSE:", resp.json())

            data = resp.json()
            if not data.get("ok", False):
                raise RuntimeError(f"Slack rejected message: {data}")

            return True

        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"Slack HTTP error {exc.response.status_code}: {exc.response.text}"
            ) from exc

        except Exception as exc:
            raise RuntimeError(f"Failed to send Slack message: {exc}") from exc

    def get_messages(self, channel_id: str, limit: int = 10) -> list[Message]:
        if self._offline or limit <= 0:
            return []

        messages: list[Message] = []

        try:
            assert self._http is not None
            resp = self._http.get(
                "/conversations.history",
                params={"channel": channel_id, "limit": limit},
            )
            resp.raise_for_status()
            data = resp.json()

            for raw in data.get("messages", []):
                messages.append(
                    SlackMessage(
                        message_id=str(raw.get("ts", "")),
                        content=str(raw.get("text", "")),
                        sender_id=str(raw.get("user", "unknown")),
                    )
                )

            return messages

        except Exception as exc:
            raise RuntimeError(f"Failed to retrieve Slack messages: {exc}") from exc

    def delete_message(self, channel_id: str, message_id: str) -> bool:
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

        except Exception as exc:
            raise RuntimeError(f"Failed to delete Slack message: {exc}") from exc

    def get_channel_members(self, channel_id: str) -> list[str]:
        if self._offline:
            return []

        try:
            assert self._http is not None
            resp = self._http.get(
                "/conversations.members",
                params={"channel": channel_id},
            )
            resp.raise_for_status()
            return list(resp.json().get("members", []))

        except Exception as exc:
            raise RuntimeError(
                f"Failed to retrieve Slack channel members: {exc}"
            ) from exc
