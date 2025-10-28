from __future__ import annotations

from typing import List, Optional

# Contract + types from slack_api (your HW1-like contract).
# We assume sync methods based on your slack_api usage and tests.
from slack_api import ChatClient, Channel, Message  # type: ignore

# Try to use validators/sanitizer if available for consistency with slack_api.
try:
    from slack_api.validators import require_channel_id  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    def require_channel_id(value: str) -> str:
        if not isinstance(value, str) or not value or not value.startswith("C"):
            raise ValueError("invalid channel id")
        return value

try:
    from slack_api.utils import sanitize_text  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    def sanitize_text(value: str, max_len: int = 4000) -> str:
        return " ".join(value.split())[:max_len]


def _mk_channel(channel_id: str, name: str) -> Channel:
    from_dict = getattr(Channel, "from_dict", None)
    if callable(from_dict):
        return from_dict({"id": channel_id, "name": name})  # type: ignore[no-any-return]
    return Channel(id=channel_id, name=name)  # type: ignore[call-arg]


def _mk_message(channel_id: str, text: str, ts: str) -> Message:
    from_dict = getattr(Message, "from_dict", None)
    if callable(from_dict):
        return from_dict({"channel_id": channel_id, "text": text, "ts": ts})  # type: ignore[no-any-return]
    return Message(channel_id=channel_id, text=text, ts=ts)  # type: ignore[call-arg]


class SlackClient(ChatClient):
    """Concrete Slack client.

    Two modes:
      - Offline (default for tests): returns deterministic data, no network.
      - Online (if configured): use Slack Web API via HTTP with a bot token.

    Online mode is activated by passing a `default_access_token` (e.g., bot token).
    You can also extend this to pull user-scoped tokens from a TokenStore in the service layer.
    """

    def __init__(self, default_access_token: Optional[str] = None) -> None:
        self._token = default_access_token

    # ---------- Offline (deterministic) behaviors always work ----------
    def health(self) -> bool:  # type: ignore[override]
        return True

    def list_channels(self) -> List[Channel]:  # type: ignore[override]
        # Offline default: deterministic list
        if not self._token:
            return [
                _mk_channel("C001", "general"),
                _mk_channel("C002", "random"),
            ]
        # Online mode: call Slack conversations.list
        try:
            import httpx  # lazy import
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("httpx is required for Slack Web API calls") from exc

        headers = {"Authorization": f"Bearer {self._token}"}
        url = "https://slack.com/api/conversations.list"
        with httpx.Client(timeout=15) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok", False):
                raise RuntimeError(f"Slack error: {data}")
            channels = []
            for ch in data.get("channels", []):
                cid = str(ch.get("id", ""))
                name = str(ch.get("name", ""))
                if cid:
                    channels.append(_mk_channel(cid, name or cid))
            return channels

    def post_message(self, channel_id: str, text: str) -> Message:  # type: ignore[override]
        cid = require_channel_id(channel_id)
        body = sanitize_text(text)

        # Offline default: deterministic message with fake TS
        if not self._token:
            return _mk_message(cid, body, "1740000000.000100")

        # Online mode: Slack chat.postMessage
        try:
            import httpx
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("httpx is required for Slack Web API calls") from exc

        headers = {"Authorization": f"Bearer {self._token}"}
        url = "https://slack.com/api/chat.postMessage"
        payload = {"channel": cid, "text": body}
        with httpx.Client(timeout=15) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("ok", False):
                raise RuntimeError(f"Slack error: {data}")
            ts = str(data.get("ts", ""))
            if not ts:
                # Some responses might nest the message object.
                msg = data.get("message", {})
                ts = str(msg.get("ts", "")) if isinstance(msg, dict) else ""
                if not ts:
                    ts = "0.0"
            return _mk_message(cid, body, ts)