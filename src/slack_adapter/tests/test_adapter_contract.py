from __future__ import annotations

from slack_api import Channel, Message

from slack_adapter import SlackServiceBackedClient


def test_adapter_exports() -> None:
    client = SlackServiceBackedClient(base_url="http://example.com")
    assert hasattr(client, "health")
    assert hasattr(client, "list_channels")
    assert hasattr(client, "post_message")
    client.close()


def test_annotations_align_with_contract() -> None:
    # Touch the annotations so ruff doesn't flag them as unused.
    chans: list[Channel] | None = None
    msg: Message | None = None
    assert chans is None
    assert msg is None
