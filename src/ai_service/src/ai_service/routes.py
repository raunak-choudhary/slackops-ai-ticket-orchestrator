"""
HTTP routes for the AI service.

All routes delegate to ai_api.get_client() and never touch
provider-specific logic directly.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ai_api import get_client
from ai_service.models import GenerateRequest, GenerateResponse, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy")


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate an AI response.

    Handles both conversational and structured output.
    All provider errors are sanitized.
    """
    client = get_client()

    try:
        result = client.generate_response(
            user_input=request.user_input,
            system_prompt=request.system_prompt,
            response_schema=request.response_schema,
        )
    except RuntimeError as exc:
        # Provider or execution failure — never leak internals
        raise HTTPException(
            status_code=500,
            detail="AI service failed to generate a response",
        ) from exc

    return GenerateResponse(result=result)
