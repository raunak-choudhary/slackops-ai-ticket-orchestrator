"""
Service-backed AI adapter.

Implements ai_api.AIInterface by delegating all operations
to the AI FastAPI service via the auto-generated HTTP client.
"""

from __future__ import annotations

import os
from typing import Any

import ai_api
from ai_api import AIInterface

# ✅ CORRECT generated-client import (matches Slack + TA)
from ai_service_api_client.ai_service_client import Client
from ai_service_api_client.ai_service_client.api.default import (
    generate_ai_response_ai_generate_post,
)
from ai_service_api_client.ai_service_client.models.ai_request import AIRequest


class AIServiceClient(AIInterface):
    """Concrete AIInterface implementation backed by ai_service."""

    def __init__(self, base_url: str) -> None:
        self._client = Client(base_url=base_url)

    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str | dict[str, Any]:
        """Generate an AI response via the remote AI service.

        All HTTP and transport errors are translated into ConnectionError.
        """
        request = AIRequest(
            user_input=user_input,
            system_prompt=system_prompt,
            response_schema=response_schema,
        )

        try:
            response = generate_ai_response_ai_generate_post(
                client=self._client,
                json_body=request,
            )
        except Exception as exc:
            raise ConnectionError(
                "Failed to contact AI service"
            ) from exc

        if response is None or response.result is None:
            raise ConnectionError("AI service returned no result")

        return response.result


def register() -> None:
    """Register the AI service adapter as the active AI client.

    The AI service base URL must be provided via environment variable:
    AI_SERVICE_BASE_URL
    """
    base_url = os.environ.get("AI_SERVICE_BASE_URL")
    if not base_url:
        raise RuntimeError(
            "AI_SERVICE_BASE_URL environment variable is not set"
        )

    def _get_service_client() -> AIInterface:
        return AIServiceClient(base_url=base_url)

    ai_api.get_client = _get_service_client
