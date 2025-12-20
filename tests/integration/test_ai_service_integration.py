import os
import pytest
import requests

pytestmark = [pytest.mark.integration, pytest.mark.live]

AI_SERVICE_BASE_URL = os.getenv("AI_SERVICE_BASE_URL")


def test_ai_service_generate_endpoint_live():
    assert AI_SERVICE_BASE_URL is not None, (
        "AI_SERVICE_BASE_URL must be set for live integration test"
    )

    response = requests.post(
        f"{AI_SERVICE_BASE_URL}/ai/generate",
        json={
            "user_input": "Say hello in one short sentence",
            "system_prompt": "You are a helpful assistant",
            "response_schema": None,
        },
        timeout=30,  # ⬅️ LIVE models are slower
    )

    if response.status_code != 200:
        print("Status:", response.status_code)
        print("Body:", response.text)

    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], (str, dict))
