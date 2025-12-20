import os
import time
import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_slack_non_ai_message():
    slack_service = os.environ["SLACK_SERVICE_BASE_URL"]
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    resp = httpx.post(
        f"{slack_service}/channels/{channel_id}/messages",
        json={"text": "hello team"},
        timeout=15,
    )
    assert resp.status_code == 200

    time.sleep(2)

    history = httpx.get(
        f"{slack_service}/channels/{channel_id}/messages",
        timeout=15,
    )
    messages = history.json()["messages"]

    assert not any("AI Response" in msg["text"] for msg in messages)
