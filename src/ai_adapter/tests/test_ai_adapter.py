from __future__ import annotations

from typing import Any
from unittest.mock import patch

import ai_api
import pytest

from ai_adapter.ai_adapter import AIServiceClient, register


class _FakeResponse:
    def __init__(self, result: str | dict[str, Any]) -> None:
        self.result = result


def test_register_sets_ai_client(monkeypatch: pytest.MonkeyPatch) -> None:
    """register() must override ai_api.get_client()."""
    monkeypatch.setenv("AI_SERVICE_BASE_URL", "http://test")

    register()
    client = ai_api.get_client()

    assert isinstance(client, AIServiceClient)


def test_generate_conversational_response() -> None:
    """Adapter returns string for conversational output."""
    adapter = AIServiceClient(base_url="http://test")

    with patch(
        "ai_adapter.ai_adapter.generate_ai_response_ai_generate_post",
        return_value=_FakeResponse("hello"),
    ):
        result = adapter.generate_response(
            user_input="hi",
            system_prompt="be helpful",
        )

    assert result == "hello"


def test_generate_structured_response() -> None:
    """Adapter returns dict for structured output."""
    adapter = AIServiceClient(base_url="http://test")

    with patch(
        "ai_adapter.ai_adapter.generate_ai_response_ai_generate_post",
        return_value=_FakeResponse({"intent": "NO_ACTION"}),
    ):
        result = adapter.generate_response(
            user_input="hi",
            system_prompt="extract intent",
            response_schema={"type": "object"},
        )

    assert result == {"intent": "NO_ACTION"}


def test_service_failure_is_connection_error() -> None:
    """Transport failures must raise ConnectionError."""
    adapter = AIServiceClient(base_url="http://test")

    with patch(
        "ai_adapter.ai_adapter.generate_ai_response_ai_generate_post",
        side_effect=Exception("boom"),
    ):
        with pytest.raises(ConnectionError, match="Failed to contact"):
            adapter.generate_response(
                user_input="hi",
                system_prompt="be helpful",
            )


def test_empty_service_response_raises_connection_error() -> None:
    """Missing service result must raise ConnectionError."""
    adapter = AIServiceClient(base_url="http://test")

    with patch(
        "ai_adapter.ai_adapter.generate_ai_response_ai_generate_post",
        return_value=_FakeResponse(None),
    ):
        with pytest.raises(ConnectionError, match="no result"):
            adapter.generate_response(
                user_input="hi",
                system_prompt="be helpful",
            )
