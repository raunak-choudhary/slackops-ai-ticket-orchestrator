from __future__ import annotations

from typing import Any

from gemini_impl.errors import GeminiError


class GeminiClient:
    """
    Lightweight client abstraction.
    This mirrors what a real Gemini SDK call would look like,
    but is intentionally minimal.
    """

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def generate(
        self,
        prompt: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str | dict[str, Any]:
        if not prompt:
            raise GeminiError("Prompt cannot be empty")

        # Simulated Gemini-style response
        if response_schema:
            return {
                "action": "respond",
                "content": prompt[:50],
            }

        return f"[Gemini] {system_prompt} | {prompt}"
