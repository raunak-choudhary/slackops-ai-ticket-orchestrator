"""Tests for GeminiProvider."""
from gemini_impl.provider import GeminiProvider
import pytest


@pytest.fixture(autouse=True)
def set_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set required Gemini environment variables for tests."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test")

def test_generate_simple_response() -> None:
    """Verify GeminiProvider returns a simple response."""
    provider = GeminiProvider()

    result = provider.generate_response(
        user_input="Hello",
        system_prompt="You are helpful",
    )

    assert isinstance(result, str)
    assert "Gemini" in result


def test_generate_structured_response() -> None:
    """Verify GeminiProvider returns structured output when schema is provided."""
    provider = GeminiProvider()

    schema = {"type": "object"}

    result = provider.generate_response(
        user_input="Create a ticket",
        system_prompt="Extract intent",
        response_schema=schema,
    )

    assert isinstance(result, dict)
    assert "content" in result
