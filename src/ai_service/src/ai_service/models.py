"""
Request and response models for the AI service.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    """Request payload for AI generation."""

    user_input: str
    system_prompt: str
    response_schema: dict[str, Any] | None = None


class GenerateResponse(BaseModel):
    """Response payload for AI generation."""

    result: str | dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
