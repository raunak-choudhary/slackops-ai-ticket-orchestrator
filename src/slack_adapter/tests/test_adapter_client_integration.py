import os
import sys

from slack_adapter.adapter import SlackServiceBackedClient

# ---------------------------------------------------------------------------
# Setup path to include the generated client package (for import resolution)
# ---------------------------------------------------------------------------
sys.path.append(os.path.abspath("clients/python"))


# ---------------------------------------------------------------------------
# DUMMY INFRASTRUCTURE
# ---------------------------------------------------------------------------


class DummyResponse:
    """
    Minimal stand-in for httpx.Response.
    Includes all attributes accessed by the generated client functions.
    """

    status_code = 200
    content = b"{}"
    headers = {}

    def json(self):
        return {}


class DummyHTTPXClient:
    """
    Fake httpx.Client replacement that records requests and returns DummyResponse.
    This avoids real network calls while letting us observe request intent.
    """

    def __init__(self):
        self.calls = []

    def request(self, method: str, url: str, **kwargs):
        self.calls.append((method, url, kwargs))
        return DummyResponse()


class DummyGeneratedClient:
    """
    Lightweight simulation of the generated slack_chat_service_hw2_client.Client class.
    It only exposes get_httpx_client(), matching the generated client's interface.
    """

    def __init__(self):
        self._httpx = DummyHTTPXClient()

    def get_httpx_client(self):
        return self._httpx


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------


def test_health_endpoint(monkeypatch):
    """
    Ensure adapter.health() delegates to generated client's sync() call properly.
    """

    adapter = SlackServiceBackedClient()
    adapter._client = DummyGeneratedClient()  # inject dummy client
    result = adapter.health()

    assert result is True, "Health endpoint should return True for HTTP 200"


def test_list_channels_and_post_message(monkeypatch):
    """
    Test adapter.list_channels() and post_message() using dummy responses.
    """

    # Dummy data to simulate Slack channel and message payloads
    dummy_channels = [{"id": "C123", "name": "general"}]
    dummy_message = {"id": "M001", "channel_id": "C123", "text": "Hello"}

    # DummyResponse with overriden .json() for custom payloads
    class DummyResponseChannels(DummyResponse):
        def json(self):
            return dummy_channels

    class DummyResponseMessage(DummyResponse):
        def json(self):
            return dummy_message

    # Dummy client returning above payloads depending on endpoint
    class SmartHTTPXClient(DummyHTTPXClient):
        def request(self, method: str, url: str, **kwargs):
            if url.endswith("/channels"):
                return DummyResponseChannels()
            elif url.endswith("/messages"):
                return DummyResponseMessage()
            return DummyResponse()

    class SmartClient(DummyGeneratedClient):
        def get_httpx_client(self):
            return SmartHTTPXClient()

    adapter = SlackServiceBackedClient()
    adapter._client = SmartClient()

    # Execute adapter methods
    channels = adapter.list_channels()
    message = adapter.post_message(channel_id="C123", text="Hello")

    # Assertions for channel list
    assert isinstance(channels, list)
    assert channels and channels[0].name == "general"

    # Assertions for posted message
    assert isinstance(message, object)
    assert message.text == "Hello"
    assert message.channel_id == "C123"


# ---------------------------------------------------------------------------
# ADDITIONAL CONTRACT CHECK
# ---------------------------------------------------------------------------


def test_adapter_context_manager_behavior():
    """
    Verify that context management (enter/exit) works without errors.
    """

    with SlackServiceBackedClient() as adapter:
        assert isinstance(adapter, SlackServiceBackedClient)
        adapter.close()  # no-op but should not raise
