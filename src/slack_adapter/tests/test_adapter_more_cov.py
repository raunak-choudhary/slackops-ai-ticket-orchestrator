from __future__ import annotations

import pytest

from slack_adapter.adapter import Channel, Message, ServiceAdapter, _get_id


class OnlyGetPostHTTP:
    def __init__(self) -> None:
        self.closed = False

    def get(self, url, **kwargs):
        if url == "/health":
            # No "ok"/"status" keys -> default True path
            class R:
                status_code = 200

                def json(self):
                    return {"unexpected": "shape"}

            return R()

        if url == "/channels":

            class R:
                def json(self):
                    return {"channels": [{"id": "C42", "name": "answer"}]}

            return R()

        raise AssertionError("unexpected GET")

    def post(self, url, **kwargs):
        if url == "/messages":

            class R:
                def json(self):
                    j = kwargs.get("json", {})
                    return {
                        "id": "m-42",
                        "text": j.get("text", ""),
                        "channel_id": j.get("channel_id", ""),
                        "ts": "4.2",
                    }

            return R()

        raise AssertionError("unexpected POST")

    def close(self) -> None:
        self.closed = True


class BadHTTP:  # lacks request/get/post -> triggers AttributeError in _do_request
    pass


def test_adapter_get_post_paths_and_health_variants() -> None:
    http = OnlyGetPostHTTP()
    adapter = ServiceAdapter(lambda: http)

    assert adapter.health() is True  # non-json ok/status -> default True

    chs = adapter.list_channels()
    assert len(chs) == 1
    assert isinstance(chs[0], Channel)
    assert chs[0].id == "C42"

    msg = adapter.post_message("C42", "msg")
    assert isinstance(msg, Message)
    assert msg.id == "m-42"


def test_do_request_error_branch() -> None:
    adapter = ServiceAdapter(lambda: BadHTTP())
    # exercise AttributeError path in _do_request via any public method
    with pytest.raises(AttributeError):
        adapter.list_channels()  # first call triggers _do_request -> error


def test_get_id_variants() -> None:
    assert _get_id({"message_id": "m9"}) == "m9"
    assert _get_id({"ts": "9.99"}) == "9.99"
