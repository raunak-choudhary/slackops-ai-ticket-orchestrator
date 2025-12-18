from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from openai_impl.openai_client import OpenAIClient


def test_provider_exception_is_sanitized() -> None:
    """Provider exceptions must be converted into RuntimeError."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}):
        client = OpenAIClient(api_key="test")

        with patch.object(
            client,
            "_call_openai",
            side_effect=Exception("provider exploded"),
        ):
            with pytest.raises(RuntimeError, match="AI service failed"):
                client.generate_response(
                    user_input="hi",
                    system_prompt="be helpful",
                )
