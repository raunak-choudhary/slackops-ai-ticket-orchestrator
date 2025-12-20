import os
import time
import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_slack_ai_basic_flow():
    slack_service = os.environ["SLACK_SERVICE_BASE_URL"]
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    resp = httpx.post(
        f"{slack_service}/channels/{channel_id}/messages",
        json={"text": "ai respond with hello"},
        timeout=15,
    )
    assert resp.status_code == 200

    time.sleep(2)

    history = httpx.get(
        f"{slack_service}/channels/{channel_id}/messages",
        timeout=15,
    )
    assert history.status_code == 200

    messages = history.json()["messages"]

    assert any("hello" in msg["text"].lower() for msg in messages)
