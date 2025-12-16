"""FastAPI application entry point for the AI service."""

from fastapi import FastAPI

# Import implementation to activate dependency injection
import openai_impl  # noqa: F401

from ai_service.routes import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="AI Service")

    app.include_router(router)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
