import os
import pytest

from ai_impl.ai_impl.gemini_client import GeminiClient


@pytest.mark.integration
def test_gemini_real_generate_response():
    """
    REAL Gemini integration test.

    - Calls Gemini for real
    - Skips if GEMINI_API_KEY is not set
    - CI-safe
    """

    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set; skipping real Gemini integration test")

    client = GeminiClient()

    response = client.generate_response(
        user_input="Say hello in one short sentence.",
        system_prompt="You are a helpful assistant.",
    )

    assert isinstance(response, str)
    assert len(response.strip()) > 0
