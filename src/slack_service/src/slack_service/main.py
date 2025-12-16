"""Slack service FastAPI application entry point.

This module defines the FastAPI application instance for the Slack service.
It wires together routing and metadata but does not contain any business
logic or provider-specific implementation details.

This service acts purely as an HTTP adapter on top of the abstract
chat API interface.
"""

from fastapi import FastAPI

from slack_service.routes import router


app = FastAPI(
    title="Slack Service API",
    description="HTTP service exposing chat operations via ChatInterface",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Register all service routes
app.include_router(router)


if __name__ == "__main__":
    """Run the Slack service using Uvicorn.

    This block allows the service to be started directly for local
    development and testing. In production or CI, the ASGI app
    should be served by a process manager.
    """
    import uvicorn

    uvicorn.run(
        "slack_service.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
