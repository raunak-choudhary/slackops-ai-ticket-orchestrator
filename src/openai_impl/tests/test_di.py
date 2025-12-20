from __future__ import annotations

import os
from unittest.mock import patch

import ai_api
from ai_api import AIInterface


class _FakeCompletions:
    """Fake OpenAI completions API."""

    def create(self, *args: object, **kwargs: object) -> object:
        msg = type("Msg", (), {"content": "ok"})()
        choice = type("Choice", (), {"message": msg})()
        return type("Resp", (), {"choices": [choice]})()


class _FakeOpenAI:
    """Fake OpenAI SDK client."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.chat = type("Chat", (), {"completions": _FakeCompletions()})()


def test_openai_impl_registers_ai_client() -> None:
    """Importing openai_impl must register an AIInterface implementation."""
    with (
        patch.dict(os.environ, {"OPENAI_API_KEY": "test"}),
        # IMPORTANT:
        # Patch the OpenAI symbol where it is ACTUALLY imported from.
        patch("openai.OpenAI", _FakeOpenAI),
    ):
        import openai_impl  # noqa: F401

        client = ai_api.get_client()
        assert isinstance(client, AIInterface)
