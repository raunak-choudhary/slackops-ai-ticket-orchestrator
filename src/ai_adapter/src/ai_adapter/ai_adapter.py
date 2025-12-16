"""Service-backed AI adapter implementing the AIInterface."""

from typing import Any

from ai_api.client import AIInterface
from ai_service_api_client.ai_service_client.client import Client
from ai_service_api_client.ai_service_client.models.ai_request import AIRequest


class AIAdapter(AIInterface):
    """AIInterface implementation backed by the AI service."""

    def __init__(self, base_url: str) -> None:
        self._client = Client(base_url=base_url)

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str | dict[str, Any]:
        """Generate a response by delegating to the AI service client."""
        request = AIRequest(
            user_input=user_input,
            system_prompt=system_prompt,
            response_schema=response_schema,
        )

        response = self._client.generate_ai_response(request)
        return response.result
