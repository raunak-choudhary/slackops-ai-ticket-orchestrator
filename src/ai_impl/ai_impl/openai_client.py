"""OpenAI client implementation."""

import os

from openai import OpenAI

from ai_api.ai_api.ai_interface import AIInterface


class OpenAIClient(AIInterface):
    """AI client backed by OpenAI chat completion models."""

    def __init__(self) -> None:
        """Initialize the OpenAI client using environment configuration."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            error_message = "OPENAI_API_KEY is not set in the environment"
            raise RuntimeError(error_message)

        self._client = OpenAI(api_key=api_key)

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict | None = None,
    ) -> str | dict:
        """Generate a response from OpenAI based on user input."""
        _ = response_schema  # Reserved for structured responses (future use)

        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )

        return response.choices[0].message.content
