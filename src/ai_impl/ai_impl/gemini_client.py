import os
import google.generativeai as genai
from ai_api.ai_api.ai_interface import AIInterface


class GeminiClient(AIInterface):
    def __init__(self) -> None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        genai.configure(api_key=api_key)

        # ✅ Use stable, real, account-verified model
        self._model = genai.GenerativeModel("models/gemini-flash-latest")

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict | None = None,
    ) -> str | dict:
        prompt = f"{system_prompt}\n\nUser: {user_input}"

        response = self._model.generate_content(prompt)

        return response.text
