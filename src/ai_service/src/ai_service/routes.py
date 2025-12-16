"""Routes for the AI service."""

from fastapi import APIRouter

from ai_api import get_client
from ai_service.models import AIRequest, AIResponse

router = APIRouter()


@router.post("/ai/generate", response_model=AIResponse)
def generate_ai_response(request: AIRequest) -> AIResponse:
    """Generate an AI response based on user input."""
    client = get_client()
    result = client.generate_response(
        user_input=request.user_input,
        system_prompt=request.system_prompt,
        response_schema=request.response_schema,
    )
    return AIResponse(result=result)
