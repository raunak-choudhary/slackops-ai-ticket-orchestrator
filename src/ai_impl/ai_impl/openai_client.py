import os

from openai import OpenAI

from ai_api import AIInterface


class OpenAIClient(AIInterface):
    def __init__(self) -> None:
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
