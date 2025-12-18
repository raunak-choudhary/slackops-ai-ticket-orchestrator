"""FastAPI entrypoint for the Jira ticket service."""

from __future__ import annotations

from fastapi import FastAPI

from jira_service.routes import router

app = FastAPI(
    title="Jira Service API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
