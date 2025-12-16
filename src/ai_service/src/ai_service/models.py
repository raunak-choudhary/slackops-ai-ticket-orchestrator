"""Pydantic models for the AI service."""

from typing import Any

from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    """Request model for AI generation."""

    user_input: str = Field(..., description="User-provided input text")
    system_prompt: str = Field(..., description="System prompt guiding AI behavior")
    response_schema: dict[str, Any] | None = Field(
        default=None,
        description="Optional JSON schema requesting structured output",
    )


class AIResponse(BaseModel):
    """Response model for AI generation."""

    result: str | dict[str, Any] = Field(
        ...,
        description="AI-generated response (string or structured data)",
    )
