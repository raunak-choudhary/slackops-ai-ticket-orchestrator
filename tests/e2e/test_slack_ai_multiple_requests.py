import os
import time
import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_slack_ai_multiple_requests():
    slack_service = os.environ["SLACK_SERVICE_BASE_URL"]
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    prompts = [
        "ai respond with hello",
        "ai respond with goodbye",
    ]

    for prompt in prompts:
        resp = httpx.post(
            f"{slack_service}/channels/{channel_id}/messages",
            json={"text": prompt},
            timeout=15,
        )
        assert resp.status_code == 200

    time.sleep(3)

    history = httpx.get(
        f"{slack_service}/channels/{channel_id}/messages",
        timeout=15,
    )
    messages = history.json()["messages"]

    assert any("hello" in msg["text"].lower() for msg in messages)
    assert any("goodbye" in msg["text"].lower() for msg in messages)
