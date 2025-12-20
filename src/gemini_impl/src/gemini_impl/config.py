"""Gemini configuration loader."""

from __future__ import annotations

import os


class GeminiConfig:
    """Configuration loader for Gemini provider."""

    def __init__(self) -> None:
        """Load Gemini configuration from environment variables."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

        if not self.api_key:
            error_msg = "Missing required environment variable: GEMINI_API_KEY"
            raise RuntimeError(error_msg)

