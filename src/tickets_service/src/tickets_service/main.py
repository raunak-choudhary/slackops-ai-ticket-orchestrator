"""Tickets service FastAPI application entry point."""

from fastapi import FastAPI

from tickets_service.routes import router

app = FastAPI(
    title="Tickets Service API",
    description="HTTP service exposing ticket operations via TicketsInterface",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "tickets_service.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
