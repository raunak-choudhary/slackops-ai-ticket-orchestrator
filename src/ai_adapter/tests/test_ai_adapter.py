"""Tests for the AI adapter."""

from typing import Any

from ai_adapter.ai_adapter import AIAdapter
from ai_api.client import AIInterface


def test_ai_adapter_implements_interface() -> None:
    """AIAdapter must implement AIInterface."""
    adapter = AIAdapter(base_url="http://localhost:8000")
    assert isinstance(adapter, AIInterface)


def test_generate_response_delegates(monkeypatch) -> None:
    """generate_response delegates to the generated client."""

    adapter = AIAdapter(base_url="http://localhost:8000")

    class DummyClient:
        def generate_ai_response(self, *args: Any, **kwargs: Any) -> Any:
            class DummyResponse:
                result = "ok"

            return DummyResponse()

    # Replace the generated client inside the adapter
    monkeypatch.setattr(adapter, "_client", DummyClient())

    result = adapter.generate_response(
        user_input="hi",
        system_prompt="be polite",
    )

    assert result == "ok"
