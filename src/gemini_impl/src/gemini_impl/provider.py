from __future__ import annotations

from typing import Any

from ai_api.client_abc import AIInterface
from gemini_impl.client import GeminiClient
from gemini_impl.config import GeminiConfig


class GeminiProvider(AIInterface):
    """
    Gemini implementation of the shared AIInterface.
    """

    def __init__(self) -> None:
        self._config = GeminiConfig()
        self._client = GeminiClient(api_key=self._config.api_key)

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str | dict[str, Any]:
        return self._client.generate(
            prompt=user_input,
            system_prompt=system_prompt,
            response_schema=response_schema,
        )
