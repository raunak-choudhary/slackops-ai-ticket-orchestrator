import os
from ai_api.ai_api.ai_interface import AIInterface


class OpenAIClient(AIInterface):
    def __init__(self) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI SDK is not installed. "
                "Install it or mock OpenAIClient in tests."
            ) from exc

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set in the environment")

        self._client = OpenAI(api_key=api_key)

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict | None = None,
    ) -> str | dict:
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )

        return response.choices[0].message.content
