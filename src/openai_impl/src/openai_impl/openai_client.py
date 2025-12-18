"""OpenAI-backed implementation of the AIInterface.

This component:
- Implements the OSS ai_api.AIInterface contract
- Talks directly to the OpenAI SDK
- Fails fast if OPENAI_API_KEY is missing (TA-style behavior)
- Supports both conversational output and structured JSON-schema output
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

from ai_api import AIInterface

if TYPE_CHECKING:
    from openai import OpenAI
    from openai.types.chat import ChatCompletionMessageParam


class OpenAIClient(AIInterface):
    """Concrete AIInterface implementation using OpenAI."""

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        """Initialize the OpenAI client.

        Args:
            api_key: Optional key. If omitted, reads OPENAI_API_KEY from env.
            model: Optional model override.

        Raises:
            RuntimeError: If no API key is available.
        """
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "No OpenAI API key found. Set OPENAI_API_KEY or pass api_key=..."
            )

        # Import here to keep module import light and make tests easier to patch.
        from openai import OpenAI  # noqa: PLC0415

        self._sdk: OpenAI = OpenAI(api_key=key)
        self._model = model or self.DEFAULT_MODEL

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str | dict[str, Any]:
        """Generate a response from OpenAI.

        If response_schema is provided, returns a dict that conforms to it.
        Otherwise returns a conversational string.

        Raises:
            RuntimeError: For missing credentials, SDK failures, or invalid output.
        """
        try:
            return self._call_openai(
                user_input=user_input,
                system_prompt=system_prompt,
                response_schema=response_schema,
            )
        except TimeoutError:
            raise RuntimeError(
                "AI service timed out while generating a response"
            ) from None
        except ValueError:
            raise RuntimeError(
                "AI service returned an invalid response format"
            ) from None
        except Exception:
            # Prevent leaking provider/SDK internals upstream.
            raise RuntimeError(
                "AI service failed to generate a response"
            ) from None

    def _call_openai(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None,
    ) -> str | dict[str, Any]:
        """Perform the actual OpenAI SDK call.

        Kept as an internal method so unit tests can patch it without doing real calls.
        """
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        if response_schema:
            schema_name = str(response_schema.get("name", "structured_output"))
            schema_description = str(
                response_schema.get("description", "Structured output schema")
            )
            json_schema = response_schema.get("schema", response_schema)

            if isinstance(json_schema, dict) and "additionalProperties" not in json_schema:
                json_schema["additionalProperties"] = False

            response = self._sdk.chat.completions.create(
                model=self._model,
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema_name,
                        "description": schema_description,
                        "schema": json_schema,
                        "strict": True,
                    },
                },
            )

            content = response.choices[0].message.content
            if not content:
                return {}
            loaded = json.loads(content)
            if not isinstance(loaded, dict):
                raise ValueError("Structured response is not a JSON object")
            return loaded

        response = self._sdk.chat.completions.create(
            model=self._model,
            messages=messages,
        )
        content = response.choices[0].message.content
        return "" if content is None else content
