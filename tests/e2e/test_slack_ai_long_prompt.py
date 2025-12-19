import os
import time
import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_slack_ai_long_prompt():
    slack_service = os.environ["SLACK_SERVICE_BASE_URL"]
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    prompt = (
        "ai explain what end-to-end testing means "
        "in one short paragraph"
    )

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

    assert any("end-to-end" in msg["text"].lower() for msg in messages)
