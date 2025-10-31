from slack_adapter.adapter import (
    Channel,
    Message,
    ServiceAdapter,
    ServiceBackedClient,
    _get_id,
)


class DummyHTTPXClient:
    def __init__(self):
        self.closed = False

    # unified entry point used by _do_request
    def request(self, method, url, **kwargs):
        class R:
            def __init__(self, method, url, kwargs):
                self.method = method
                self.url = url
                self.kwargs = kwargs
                self.status_code = 200

            def json(self):
                # health probe returns {"ok": True}
                if self.url == "/health":
                    return {"ok": True}
                if self.url == "/channels":
                    return {"channels": [{"id": "C9", "name": "nine"}]}
                if self.url == "/messages":
                    payload = self.kwargs.get("json", {})
                    return {
                        "id": "m-1",
                        "text": payload.get("text", ""),
                        "channel_id": payload.get("channel_id", ""),
                        "ts": "1.23",
                    }
                return {}

        return R(method, url, kwargs)

    def close(self):
        self.closed = True


def test_health_list_and_post_paths() -> None:
    http = DummyHTTPXClient()
    adapter = ServiceAdapter(lambda: http)

    assert adapter.health() is True

    chs = adapter.list_channels()
    assert len(chs) == 1 and isinstance(chs[0], Channel) and chs[0].id == "C9"

    msg = adapter.post_message("C9", "hello")
    assert isinstance(msg, Message)
    assert msg.channel_id == "C9" and msg.id == "m-1"


def test_get_id_and_public_client_close_and_identifier() -> None:
    http = DummyHTTPXClient()
    client = ServiceBackedClient(base_url="http://test", http=http)

    # _get_id coverage variants
    assert _get_id({"id": "x"}) == "x"
    assert _get_id(Message(message_id="m2", text="t", channel_id="c", ts="1.0")) == "m2"

    # message_identifier happy path
    assert client.message_identifier({"id": "ok"}) == "ok"

    # message_identifier error path
    try:
        client.message_identifier({})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    # __enter__/__exit__/close path
    with client as c2:
        assert c2 is client
    assert http.closed is True
