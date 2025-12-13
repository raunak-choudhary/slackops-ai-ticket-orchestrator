import os
import pytest

from ai_impl.ai_impl.openai_client import OpenAIClient


@pytest.mark.integration
def test_openai_real_generate_response():
    """
    REAL OpenAI integration test.

    - Calls OpenAI for real
    - Skips if OPENAI_API_KEY is not set
    - CI-safe
    """

    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set; skipping real OpenAI integration test")

    client = OpenAIClient()

    response = client.generate_response(
        user_input="Say hello in one short sentence.",
        system_prompt="You are a helpful assistant.",
    )

    assert isinstance(response, str)
    assert len(response.strip()) > 0
