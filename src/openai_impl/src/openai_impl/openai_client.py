"""OpenAI-backed implementation of the AIInterface."""

import os
from typing import Any

from openai import OpenAI

from ai_api.client import AIInterface


class OpenAIClient(AIInterface):
    """Concrete AI client implementation using OpenAI."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is required")

        self._client = OpenAI(api_key=api_key)

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str | dict[str, Any]:
        """Generate a response from OpenAI.

        If response_schema is provided, a structured JSON response is requested.
        Otherwise, a conversational text response is returned.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        if response_schema is not None:
            completion = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": response_schema,
                },
            )
            return completion.choices[0].message.parsed

        completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return completion.choices[0].message.content
