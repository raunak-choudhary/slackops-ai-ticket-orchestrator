"""Gemini AI client implementation."""

import os

import google.generativeai as genai

from ai_api.ai_api.ai_interface import AIInterface


class GeminiClient(AIInterface):
    """AI client backed by Google's Gemini models."""

    def __init__(self) -> None:
        """Initialize the Gemini client using environment configuration."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            error_message = "GEMINI_API_KEY is not set"
            raise RuntimeError(error_message)

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel("models/gemini-flash-latest")

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict | None = None,
    ) -> str | dict:
        """Generate a response from Gemini based on user input."""
        _ = response_schema  # Required for interface compatibility

        prompt = f"{system_prompt}\n\nUser: {user_input}"
        response = self._model.generate_content(prompt)

        return response.text
