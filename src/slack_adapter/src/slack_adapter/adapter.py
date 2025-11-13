"""Slack adapter: typed HTTP client facade over the Slack Chat Service.

Public surface:
- Channel, Message
- ServiceAdapter, ServiceBackedClient, SlackServiceBackedClient
- _get_id (utility used in tests)
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Self, runtime_checkable

import httpx

from slack_api import Channel as _SlackChannel  # type: ignore[import]

if TYPE_CHECKING:
    # Only imported for type hints (Ruff TC003 wants this behind TYPE_CHECKING)
    from types import TracebackType

HTTP_OK = 200


@runtime_checkable
class _ResponseLike(Protocol):
    """Minimal response surface needed by the adapter."""

    status_code: int

    def json(self) -> object:
        """Return a JSON-decoded object (dict, list, etc.)."""
        ...


@runtime_checkable
class _HTTPClientLike(Protocol):
    """Minimal httpx-like client surface used by the adapter."""

    def request(self, method: str, url: str, **kwargs: object) -> _ResponseLike: ...
    def get(self, url: str, **kwargs: object) -> _ResponseLike: ...
    def post(self, url: str, **kwargs: object) -> _ResponseLike: ...
    def close(self) -> None: ...


def _as_mapping(obj: object) -> Mapping[str, object] | None:
    """Return a mapping view for dict-like or object-like inputs."""
    if isinstance(obj, Mapping):
        return obj
    try:
        # Works for dataclasses and simple objects with __dict__
        return dict(vars(obj))  # type: ignore[arg-type]
    except (TypeError, AttributeError):
        return None


def _maybe_get(mapping: Mapping[str, object], key: str) -> object | None:
    """Safe getter that returns None when the key is absent."""
    return mapping.get(key)


def _get_id(obj: object) -> str:
    """Extract identifier in order: 'id' -> 'message_id' -> 'ts'."""
    mapping = _as_mapping(obj)
    if mapping is not None:
        for key in ("id", "message_id", "ts"):
            val = _maybe_get(mapping, key)
            if isinstance(val, str) and val:
                return val
    msg = "could not extract identifier from object"
    raise ValueError(msg)


# ---------------------------------------------------------------------------
# Public models exported by this module
# ---------------------------------------------------------------------------

Channel = _SlackChannel


@dataclass(frozen=True)
class Message:
    """Lightweight message model compatible with tests.

    The internal slack_api.Message uses (channel_id, text, ts). Tests also
    construct Message(message_id=...) and access .id, so we provide both.
    """

    message_id: str
    text: str
    channel_id: str
    ts: str

    @property
    def id(self) -> str:
        """Alias for message_id used by some tests."""
        return self.message_id


# ---------------------------------------------------------------------------
# Base client with context manager semantics
# ---------------------------------------------------------------------------


class ServiceBackedClient:
    """Thin HTTP wrapper with context manager semantics.

    Parameters
    ----------
    base_url:
        Base URL used when constructing a real HTTP client.
    http:
        HTTP client instance implementing the _HTTPClientLike protocol.

    """

    def __init__(self, base_url: str, http: _HTTPClientLike) -> None:
        """Initialize with a base URL and an HTTP client."""
        self._base_url = base_url.rstrip("/")
        self._http = http

    def __enter__(self) -> Self:
        """Enter the context manager and return self."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the context manager and close the HTTP client."""
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def message_identifier(self, payload: object) -> str:
        """Return an identifier extracted from a message-like payload."""
        return _get_id(payload)


# ---------------------------------------------------------------------------
# Concrete Slack client
# ---------------------------------------------------------------------------


class SlackServiceBackedClient(ServiceBackedClient):
    """Adapter for the Slack Chat Service HTTP API.

    If `http` is None, an httpx.Client(base_url=...) is created.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        http: _HTTPClientLike | None = None,
    ) -> None:
        """Create a SlackServiceBackedClient with optional custom HTTP client."""
        if http is None:
            http = httpx.Client(base_url=base_url)
        super().__init__(base_url=base_url, http=http)  # type: ignore[arg-type]

    # -----------------------
    # Public API
    # -----------------------

    def health(self) -> bool:
        """Probe service health via GET /health with tolerant JSON handling."""
        resp = self._http.get("/health")
        if getattr(resp, "status_code", 0) != HTTP_OK:
            return False
        body = resp.json()
        mapping = _as_mapping(body)
        if mapping is None:
            return True
        ok_val = _maybe_get(mapping, "ok")
        if isinstance(ok_val, bool):
            return ok_val
        status_val = _maybe_get(mapping, "status")
        if isinstance(status_val, str):
            return status_val.lower() == "ok"
        return True

    def list_channels(self) -> list[Channel]:
        """Return channels via GET /channels, tolerant to shape variants."""
        resp = self._http.get("/channels")
        data = resp.json()

        channels_list: list[Mapping[str, object]]
        if isinstance(data, list):
            channels_list = [m for m in data if isinstance(m, Mapping)]
        else:
            mapping = _as_mapping(data) or {}
            raw = mapping.get("channels")
            channels_list = list(raw) if isinstance(raw, list) else []

        result: list[Channel] = []
        for item in channels_list:
            cid = item.get("id")
            name = item.get("name")
            if isinstance(cid, str) and isinstance(name, str):
                result.append(Channel(id=cid, name=name))
        return result

    def post_message(self, channel_id: str, text: str) -> Message:
        """Post a message via POST /messages and return a typed Message."""
        payload: Mapping[str, object] = {"channel_id": channel_id, "text": text}
        resp = self._http.post("/messages", json=payload)
        data = resp.json()
        mapping = _as_mapping(data) or {}
        identifier = _get_id(mapping)
        ts_val = mapping.get("ts")
        ts = str(ts_val) if isinstance(ts_val, (str, int, float)) else ""
        return Message(message_id=identifier, text=text, channel_id=channel_id, ts=ts)


# ---------------------------------------------------------------------------
# Lightweight façade used in tests
# ---------------------------------------------------------------------------


class ServiceAdapter:
    """Small façade that owns an HTTP client created by a factory.

    Mirrors the same public methods as SlackServiceBackedClient.
    """

    def __init__(self, http_factory: Callable[[], _HTTPClientLike]) -> None:
        """Create an adapter that lazily instantiates an HTTP client."""
        self._http_factory = http_factory
        self._http: _HTTPClientLike | None = None

    def _ensure_http(self) -> _HTTPClientLike:
        if self._http is None:
            self._http = self._http_factory()
        return self._http

    def _do_request(self, method: str, url: str, **kwargs: object) -> _ResponseLike:
        http = self._ensure_http()
        if hasattr(http, "request"):
            return http.request(method, url, **kwargs)  # type: ignore[return-value]
        if method.upper() == "GET" and hasattr(http, "get"):
            return http.get(url, **kwargs)  # type: ignore[return-value]
        if method.upper() == "POST" and hasattr(http, "post"):
            return http.post(url, **kwargs)  # type: ignore[return-value]
        msg = "HTTP client lacks request/get/post methods"
        raise AttributeError(msg)

    def health(self) -> bool:
        """Probe service health via GET /health."""
        resp = self._do_request("GET", "/health")
        if getattr(resp, "status_code", HTTP_OK) != HTTP_OK:
            return False
        body = resp.json()
        mapping = _as_mapping(body)
        if mapping is None:
            return True
        ok_val = _maybe_get(mapping, "ok")
        if isinstance(ok_val, bool):
            return ok_val
        status_val = _maybe_get(mapping, "status")
        if isinstance(status_val, str):
            return status_val.lower() == "ok"
        return True

    def list_channels(self) -> list[Channel]:
        """Fetch channel list via GET /channels."""
        resp = self._do_request("GET", "/channels")
        data = resp.json()

        if isinstance(data, list):
            raw_list = [m for m in data if isinstance(m, Mapping)]
        else:
            mapping = _as_mapping(data) or {}
            chs = mapping.get("channels")
            raw_list = list(chs) if isinstance(chs, list) else []

        out: list[Channel] = []
        for item in raw_list:
            cid = item.get("id")
            name = item.get("name")
            if isinstance(cid, str) and isinstance(name, str):
                out.append(Channel(id=cid, name=name))
        return out

    def post_message(self, channel_id: str, text: str) -> Message:
        """Post a message via POST /messages."""
        resp = self._do_request(
            "POST",
            "/messages",
            json={"channel_id": channel_id, "text": text},
        )
        data = resp.json()
        mapping = _as_mapping(data) or {}
        identifier = _get_id(mapping)
        ts_val = mapping.get("ts")
        ts = str(ts_val) if isinstance(ts_val, (str, int, float)) else ""
        return Message(message_id=identifier, text=text, channel_id=channel_id, ts=ts)

    def close(self) -> None:
        """Close the underlying HTTP client (once created)."""
        http = self._ensure_http()
        http.close()


# Explicit public API (sorted for Ruff RUF022 within the module)
__all__ = [
    "HTTP_OK",
    "Channel",
    "Message",
    "ServiceAdapter",
    "ServiceBackedClient",
    "SlackServiceBackedClient",
    "_HTTPClientLike",
    "_ResponseLike",
    "_as_mapping",
    "_get_id",
    "_maybe_get",
]

