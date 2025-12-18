from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from openai_impl.openai_client import OpenAIClient


def _make_client() -> OpenAIClient:
    """Create a real OpenAIClient for unit testing."""
    return OpenAIClient(api_key="test")


def test_generate_response_returns_string() -> None:
    """generate_response returns a string for conversational output."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}):
        client = _make_client()

        with patch.object(client, "_call_openai", return_value="hello world"):
            result = client.generate_response(
                user_input="hi",
                system_prompt="be helpful",
                response_schema=None,
            )

        assert result == "hello world"


def test_generate_response_returns_dict_for_schema() -> None:
    """generate_response returns dict for structured output mode."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}):
        client = _make_client()

        schema = {
            "name": "intent",
            "description": "Extract intent",
            "schema": {
                "type": "object",
                "properties": {"action": {"type": "string"}},
                "required": ["action"],
                "additionalProperties": False,
            },
        }

        with patch.object(client, "_call_openai", return_value={"action": "NO_ACTION"}):
            result = client.generate_response(
                user_input="hello",
                system_prompt="be helpful",
                response_schema=schema,
            )

        assert result == {"action": "NO_ACTION"}


def test_missing_api_key_raises() -> None:
    """Initialization fails when no API key is provided."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(RuntimeError, match="OPENAI_API_KEY|API key"):
            OpenAIClient()
