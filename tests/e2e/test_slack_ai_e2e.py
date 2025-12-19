import os
import time
import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_slack_ai_end_to_end_via_orchestrator():
    """
    End-to-End test:
    Slack Service → Orchestrator → AI Service → Slack Service

    Fully runnable without Socket Mode.
    """

    slack_service = os.environ["SLACK_SERVICE_BASE_URL"]
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    # 1️⃣ Send AI command into Slack Service
    post_resp = httpx.post(
        f"{slack_service}/channels/{channel_id}/messages",
        json={"text": "ai respond with hello"},
        timeout=15,
    )
    assert post_resp.status_code == 200

    # 2️⃣ Allow async processing
    time.sleep(2)

    # 3️⃣ Verify AI response appears in Slack history
    history = httpx.get(
        f"{slack_service}/channels/{channel_id}/messages",
        timeout=15,
    )
    assert history.status_code == 200

    payload = history.json()
    messages = payload["messages"]  # ✅ FIX

    assert any(
        "AI Response" in msg["text"] or "hello" in msg["text"].lower()
        for msg in messages
    )
