"""Tests for AI API dependency injection behavior."""

from __future__ import annotations

import importlib

import pytest

import ai_api
import ai_api.client as ai_client
from ai_api.client import AIInterface


def test_get_client_exists() -> None:
    """ai_api must expose get_client."""
    assert hasattr(ai_api, "get_client")
    assert callable(ai_api.get_client)


def test_get_client_raises_when_not_registered() -> None:
    """Calling get_client without a registered implementation should fail."""
    # Reset DI state to ensure no provider has monkey-patched get_client
    importlib.reload(ai_client)

    with pytest.raises(RuntimeError):
        ai_client.get_client()


def test_get_client_return_type_after_registration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """After DI registration, get_client should return an AIInterface."""

    class DummyAIClient(AIInterface):
        """Minimal dummy AI client for DI testing."""

        def generate_response(
            self,
            user_input: str,
            system_prompt: str,
            response_schema: dict | None = None,
        ) -> str:
            return "ok"

    monkeypatch.setattr(ai_client, "get_client", lambda: DummyAIClient())

    client = ai_client.get_client()
    assert isinstance(client, AIInterface)
