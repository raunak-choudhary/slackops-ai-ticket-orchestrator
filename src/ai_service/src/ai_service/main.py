"""
FastAPI service exposing the AI API.

This service:
- Explicitly activates AI dependency injection
- Exposes AI functionality over HTTP
- Does NOT depend on provider-specific implementations
"""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI

import openai_impl  # noqa: F401

from ai_service.routes import router


def _configure_logging() -> None:
    """Configure service logging."""
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=level)
    logging.getLogger(__name__).info("Logging configured | level=%s", level)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    _configure_logging()

    app = FastAPI(title="AI Service")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(router)

    logging.getLogger(__name__).info("AI Service application created")
    return app


app = create_app()
