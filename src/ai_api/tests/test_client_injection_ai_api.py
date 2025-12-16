"""Tests for AI API dependency injection behavior."""

import pytest

import ai_api
from ai_api.client import AIInterface


def test_get_client_exists() -> None:
    """ai_api must expose get_client."""
    assert hasattr(ai_api, "get_client")
    assert callable(ai_api.get_client)


def test_get_client_raises_when_not_registered() -> None:
    """Calling get_client without a registered implementation should fail."""
    with pytest.raises(RuntimeError):
        ai_api.get_client()


def test_get_client_return_type_after_registration(monkeypatch: pytest.MonkeyPatch) -> None:
    """After DI registration, get_client should return an AIInterface."""

    class DummyAIClient(AIInterface):
        def generate_response(
            self,
            user_input: str,
            system_prompt: str,
            response_schema: dict | None = None,
        ) -> str:
            return "ok"

    monkeypatch.setattr(ai_api, "get_client", lambda: DummyAIClient())

    client = ai_api.get_client()
    assert isinstance(client, AIInterface)
