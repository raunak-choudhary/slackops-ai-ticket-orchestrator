"""Tests for AIInterface protocol compliance."""

from typing import Any

import pytest

from ai_api.client import AIInterface


class CompliantAIClient(AIInterface):
    """Minimal compliant AI client implementation for testing."""

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str:
        return "ok"


def test_compliant_client_is_instance_of_interface() -> None:
    """A compliant implementation should be an instance of AIInterface."""
    client = CompliantAIClient()
    assert isinstance(client, AIInterface)


def test_compliant_client_generate_response_callable() -> None:
    """generate_response should be callable on compliant client."""
    client = CompliantAIClient()
    result = client.generate_response(
        user_input="hi",
        system_prompt="be polite",
        response_schema=None,
    )
    assert result == "ok"


def test_non_compliant_client_cannot_be_instantiated() -> None:
    """Missing abstract methods should prevent instantiation."""

    class IncompleteAIClient(AIInterface):
        pass

    with pytest.raises(TypeError):
        IncompleteAIClient()  # type
