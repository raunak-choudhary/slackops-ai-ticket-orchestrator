import logging
from fastapi import APIRouter, HTTPException

import ai_api
from ai_service.models import GenerateRequest, GenerateResponse, HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ai/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    logger.info("AI generate request received")

    client = ai_api.get_client()  # ✅ dynamically resolved

    try:
        result = client.generate_response(
            user_input=request.user_input,
            system_prompt=request.system_prompt,
            response_schema=request.response_schema,
        )
    except RuntimeError as exc:
        logger.exception("AI generation failed (sanitized)")
        raise HTTPException(
            status_code=500,
            detail="AI service failed to generate a response",
        ) from exc

    return GenerateResponse(result=result)
