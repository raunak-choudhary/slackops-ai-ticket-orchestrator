"""
Additional unit tests for openai_impl.openai_client to increase branch coverage.
No real OpenAI calls are made.
"""

from unittest.mock import Mock, patch

import pytest

from openai_impl.openai_client import OpenAIClient


@pytest.mark.unit
def test_generate_response_timeout_error() -> None:
    client = OpenAIClient(api_key="fake-key")

    with patch.object(
        client,
        "_call_openai",
        side_effect=TimeoutError("timeout"),
    ):
        with pytest.raises(RuntimeError) as exc:
            client.generate_response(
                user_input="hi",
                system_prompt="sys",
            )

    assert "timed out" in str(exc.value)


@pytest.mark.unit
def test_generate_response_value_error() -> None:
    client = OpenAIClient(api_key="fake-key")

    with patch.object(
        client,
        "_call_openai",
        side_effect=ValueError("bad format"),
    ):
        with pytest.raises(RuntimeError) as exc:
            client.generate_response(
                user_input="hi",
                system_prompt="sys",
            )

    assert "invalid response format" in str(exc.value)


@pytest.mark.unit
def test_call_openai_structured_output_empty_content() -> None:
    client = OpenAIClient(api_key="fake-key")

    mock_message = Mock()
    mock_message.content = None

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_response = Mock()
    mock_response.choices = [mock_choice]

    with patch.object(
        client._sdk.chat.completions,
        "create",
        return_value=mock_response,
    ):
        result = client._call_openai(
            user_input="hi",
            system_prompt="sys",
            response_schema={
                "name": "schema",
                "schema": {"type": "object"},
            },
        )

    assert result == {}
