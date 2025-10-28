from __future__ import annotations

import anyio
import httpx
import pytest
from httpx import BaseTransport, Request, Response

from slack_adapter import SlackServiceBackedClient

# Import FastAPI app in-process so tests run without a real server.
try:
    from slack_service.app import app  # type: ignore[import]
except Exception as exc:  # pragma: no cover
    app = None  # type: ignore[assignment]
    _import_error: Exception | None = exc
else:
    _import_error = None


pytestmark = pytest.mark.skipif(
    app is None,
    reason=f"slack_service not importable: {_import_error}",
)


class SyncASGITransport(BaseTransport):
    """
    Synchronous wrapper around httpx's async ASGITransport (httpx>=0.27).
    It converts the async response into a fully-materialized sync Response,
    ensuring response.stream is a SyncByteStream (what httpx.Client expects).
    """

    def __init__(self, asgi_app) -> None:  # type: ignore[no-untyped-def]
        from httpx import ASGITransport as _ASGITransport

        self._async = _ASGITransport(app=asgi_app)

    def handle_request(self, request: Request) -> Response:
        async def _go() -> Response:
            # Get async response from ASGI transport
            async_resp: Response = await self._async.handle_async_request(request)  # type: ignore[assignment]
            # Read the entire body so we can build a sync Response
            content = await async_resp.aread()
            return Response(
                status_code=async_resp.status_code,
                headers=async_resp.headers,
                content=content,
                request=request,
                extensions=async_resp.extensions,
            )

        return anyio.run(_go)

    def close(self) -> None:
        anyio.run(self._async.aclose)


def _adapter_against_inmemory_service() -> SlackServiceBackedClient:
    assert app is not None
    transport = SyncASGITransport(app)
    http = httpx.Client(transport=transport, base_url="http://test")
    return SlackServiceBackedClient(base_url="http://test", http=http)


def test_health_true() -> None:
    client = _adapter_against_inmemory_service()
    try:
        assert client.health() is True
    finally:
        client.close()


def test_list_channels_expected_ids() -> None:
    client = _adapter_against_inmemory_service()
    try:
        channels = client.list_channels()
        ids = {c.id for c in channels}
        assert {"C001", "C002"}.issubset(ids)
    finally:
        client.close()


def test_post_message_returns_ts() -> None:
    client = _adapter_against_inmemory_service()
    try:
        msg = client.post_message("C001", "hello")
        assert msg.channel_id == "C001"
        assert isinstance(msg.ts, str) and len(msg.ts) > 0
    finally:
        client.close()