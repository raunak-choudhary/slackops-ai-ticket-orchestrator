from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import TYPE_CHECKING, Any, Protocol, cast

# -------- Generated client (optional, dynamic import) -----------------
if TYPE_CHECKING:

    class _GenClientProto(Protocol):
        def __init__(
            self,
            *,
            base_url: str,
            headers: dict[str, str] | None,
            cookies: Any | None,
            timeout: float,
            verify_ssl: bool,
        ) -> None: ...

        def get_httpx_client(self) -> Any: ...


def _load_generated_client() -> type[_GenClientProto] | None:
    """
    Import the generated client dynamically so the package works
    even if it isn’t installed yet.
    """
    try:
        mod = import_module("slack_chat_service_hw2_client.client")
        client_cls = mod.Client
        return cast(type[_GenClientProto], client_cls)
    except Exception:
        return None


# -------- Domain models -----------------------------------------------
@dataclass(frozen=True)
class Channel:
    channel_id: str
    name: str

    @property
    def id(self) -> str:
        # tests access c.id
        return self.channel_id

    @staticmethod
    def from_any(data: Any) -> Channel:
        if isinstance(data, dict):
            cid = (
                data.get("id")
                or data.get("channel_id")
                or data.get("channelId")
                or data.get("name")
                or ""
            )
            name = data.get("name") or str(cid)
        else:
            cid, name = "", ""
        return Channel(channel_id=str(cid), name=str(name))


@dataclass(frozen=True)
class Message:
    message_id: str
    text: str
    channel_id: str
    ts: str

    @property
    def id(self) -> str:
        return self.message_id

    @staticmethod
    def from_any(data: Any) -> Message:
        if isinstance(data, dict):
            mid = data.get("id") or data.get("message_id") or data.get("ts") or ""
            txt = data.get("text") or ""
            cid = data.get("channel_id") or data.get("channel") or ""
            ts = data.get("ts") or str(mid) or ""
        else:
            mid, txt, cid, ts = "", "", "", ""
        return Message(
            message_id=str(mid),
            text=str(txt),
            channel_id=str(cid),
            ts=str(ts),
        )


def _get_id(obj: Any) -> str:
    if hasattr(obj, "id"):
        return str(obj.id)
    if hasattr(obj, "message_id"):
        return str(obj.message_id)
    if isinstance(obj, dict):
        return str(obj.get("id") or obj.get("message_id") or obj.get("ts") or "")
    return ""


# -------- HTTP helper --------------------------------------------------
def _do_request(http: Any, method: str, url: str, **kwargs: Any) -> Any:
    """
    Prefer a single .request() (used by DummyHTTPXClient in tests),
    fall back to httpx-style .get/.post.
    """
    if hasattr(http, "request"):
        return http.request(method, url, **kwargs)
    up = method.upper()
    if up == "GET" and hasattr(http, "get"):
        return http.get(url, **kwargs)
    if up == "POST" and hasattr(http, "post"):
        return http.post(url, **kwargs)
    msg = "Provided http client lacks request/get/post methods"
    raise AttributeError(msg)


# -------- Internal adapter (maps endpoints to models) ------------------
class ServiceAdapter:
    def __init__(self, get_http: Callable[[], Any]) -> None:
        self._get_http = get_http

    def health(self) -> bool:
        http = self._get_http()
        r = _do_request(http, "GET", "/health")
        try:
            data = r.json()
        except Exception:
            return getattr(r, "status_code", None) == 200
        if isinstance(data, dict):
            if "ok" in data:
                return bool(data.get("ok"))
            if "status" in data:
                return str(data.get("status", "")).lower() == "ok"
        return True

    def list_channels(self) -> list[Channel]:
        http = self._get_http()
        r = _do_request(http, "GET", "/channels")
        try:
            data = r.json()
        except Exception:
            data = []
        items: list[Any] = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and isinstance(data.get("channels"), list):
            items = data["channels"]
        return [Channel.from_any(it) for it in items]

    def post_message(self, channel_id: str, text: str) -> Message:
        http = self._get_http()
        payload = {"channel_id": channel_id, "text": text}
        r = _do_request(http, "POST", "/messages", json=payload)
        try:
            data = r.json()
        except Exception:
            data = {}
        if isinstance(data, dict):
            return Message.from_any(data)
        return Message(message_id="", text=text, channel_id=channel_id, ts="")


# -------- Public client ------------------------------------------------
class ServiceBackedClient:
    """
    HW1+HW2-compatible client.

    - Accepts `http` (for in-memory ASGI transport in tests)
    - Uses generated client if available
    - Exposes .health(), .list_channels(), .post_message(), .close()
    - Works as a context manager
    - Exposes `_client` so tests can inject a DummyGeneratedClient
    """

    def __init__(
        self,
        base_url: str | None = None,
        *,
        token: str | None = None,
        timeout: float | None = 10.0,
        verify_ssl: bool = True,
        default_headers: dict[str, str] | None = None,
        http: Any | None = None,
    ) -> None:
        headers: dict[str, str] = {}
        if default_headers:
            headers.update(default_headers)
        if token:
            headers.setdefault("Authorization", f"Bearer {token}")

        self._base_url = (base_url or "http://test").rstrip("/")
        self._http: Any | None = http
        self._client: _GenClientProto | None = None

        if self._http is None:
            Gen = _load_generated_client()
            if Gen is not None:
                self._client = Gen(
                    base_url=self._base_url,
                    headers=headers or None,
                    cookies=None,
                    timeout=timeout if timeout is not None else 10.0,
                    verify_ssl=verify_ssl,
                )
            else:
                # Create a plain httpx client lazily in _get_http()
                self._http = None

        self._adapter = ServiceAdapter(self._get_http)

    # Resolve an httpx-like client on demand
    def _get_http(self) -> Any:
        if self._client is not None and hasattr(self._client, "get_httpx_client"):
            return self._client.get_httpx_client()

        if self._http is None:
            try:
                import httpx  # local import to keep it optional
            except Exception as exc:  # pragma: no cover
                msg = "httpx is required for ServiceBackedClient"
                raise RuntimeError(msg) from exc
            self._http = httpx.Client(base_url=self._base_url)
        return self._http

    # Public API
    def health(self) -> bool:
        return self._adapter.health()

    def list_channels(self) -> list[Channel]:
        return self._adapter.list_channels()

    def post_message(self, channel_id: str, text: str) -> Message:
        return self._adapter.post_message(channel_id, text)

    # Lifecycle
    def close(self) -> None:
        http = self._get_http()
        if hasattr(http, "close"):
            try:
                http.close()
            except Exception:
                pass

    def __enter__(self) -> ServiceBackedClient:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    @staticmethod
    def message_identifier(message: Any) -> str:
        ident = _get_id(message)
        if not ident:
            raise ValueError("Message must have id or message_id")
        return ident


# Back-compat export
SlackServiceBackedClient = ServiceBackedClient
