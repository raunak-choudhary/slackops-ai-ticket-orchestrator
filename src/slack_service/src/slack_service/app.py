from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Slack Chat Service (HW2)")

@app.get("/health")
def health():
    return {"status": "ok"}
