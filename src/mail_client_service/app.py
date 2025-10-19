from __future__ import annotations

from fastapi import FastAPI

from .routes import messages

app = FastAPI(title="Mail Client Service", version="0.1.0")

# The router itself has no prefix; mount it at /messages here
app.include_router(messages.router, prefix="/messages", tags=["messages"])