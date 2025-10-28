from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar, cast

import httpx
from slack_api import Channel, ChatClient, Message  # contract + types

T = TypeVar("T")


def _from_dict_or_init(cls: type[T], data: dict[str, Any]) -> T:
    """
    Construct a typed object from a dict:
      - Prefer classmethod `from_dict` if present
      - Else try direct construction with kwargs
    """
    candidate: Callable[[dict[str, Any]], Any] | None = getattr(cls, "from_dict", None)
    if callable(candidate):
        return cast(T, candidate(data))
    return cast(T, cls(**data))  # type: ignore[call-arg]


class SlackServiceBackedClient(ChatClient):
    """
    A ChatClient implementation that delegates to the local FastAPI Slack service over HTTP.
    """

    def __init__(
        self,
        base_url: str,
        http: httpx.Client | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = http or httpx.Client(timeout=timeout)

    # ---- lifecycle ---------------------------------------------------------

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> SlackServiceBackedClient:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()

    # ---- ChatClient contract -----------------------------------------------

    def health(self) -> bool:
        resp = self._http.get(f"{self._base_url}/health")
        return resp.status_code == 200

    def list_channels(self) -> list[Channel]:
        resp = self._http.get(f"{self._base_url}/channels")
        resp.raise_for_status()
        payload = resp.json()
        # tolerate either bare list or {"channels": [...]}
        raw_list: Any = payload.get("channels", payload) if isinstance(payload, dict) else payload
        if not isinstance(raw_list, list):
            raise ValueError("Unexpected channels payload shape")

        channels: list[Channel] = [
            _from_dict_or_init(Channel, cast(dict[str, Any], item))
            for item in raw_list
        ]
        return channels

    def post_message(self, channel_id: str, text: str) -> Message:
        resp = self._http.post(
            f"{self._base_url}/messages",
            json={"channel_id": channel_id, "text": text},
        )
        resp.raise_for_status()
        data = resp.json()
        # tolerate either bare dict or {"message": {...}}
        raw_msg: Any = data.get("message", data) if isinstance(data, dict) else data
        if not isinstance(raw_msg, dict):
            raise ValueError("Unexpected message payload shape")
        return _from_dict_or_init(Message, cast(dict[str, Any], raw_msg))
