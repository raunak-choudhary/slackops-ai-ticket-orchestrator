"""
FastAPI service exposing the AI API.

This service:
- Explicitly activates AI dependency injection
- Exposes AI functionality over HTTP
- Does NOT depend on provider-specific implementations
"""

from __future__ import annotations

from fastapi import FastAPI

# -------------------------
# CRITICAL: Activate DI
# -------------------------
# Importing the implementation registers it with ai_api.get_client().
# This must be explicit (TA requirement).
import openai_impl  # noqa: F401

from ai_service.routes import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="AI Service")

    app.include_router(router)

    return app


app = create_app()
