import os
import httpx
import pytest
pytestmark = pytest.mark.integration


def test_slack_service_post_and_list_messages():
    base_url = os.environ["SLACK_SERVICE_BASE_URL"]
    channel_id = os.environ["SLACK_TEST_CHANNEL_ID"]

    post_resp = httpx.post(
        f"{base_url}/channels/{channel_id}/messages",
        json={"text": "integration test message"},
        timeout=15,
    )
    assert post_resp.status_code == 200

    list_resp = httpx.get(
        f"{base_url}/channels/{channel_id}/messages",
        params={"limit": 5},
        timeout=15,
    )
    assert list_resp.status_code == 200

    messages = list_resp.json()["messages"]
    assert any("integration test message" in m["text"] for m in messages)
