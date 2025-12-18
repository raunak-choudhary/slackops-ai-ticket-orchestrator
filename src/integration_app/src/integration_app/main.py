from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool

from integration_app.slack_entry import SlackEventHandler
from integration_app.config import load_config

app = FastAPI(title="HW3 Integration App")


@app.on_event("startup")
def startup() -> None:
    """
    Application startup hook.

    Loads and validates required environment configuration early so failures
    are loud and deterministic, rather than surfacing later mid-request.
    """
    print("INTEGRATION APP STARTUP")
    load_config()
    print("INTEGRATION APP CONFIG LOADED")


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/slack/events")
async def slack_events(request: Request) -> JSONResponse:
    """
    Slack Events API entry point.

    Slack requires HTTP 200 responses even on internal failures. Errors must be
    logged for observability, but the HTTP response should remain 200.
    """
    payload = await request.json()

    # Slack URL verification MUST return immediately
    if payload.get("type") == "url_verification":
        return JSONResponse(
            status_code=200,
            content={"challenge": payload["challenge"]},
        )

    handler = SlackEventHandler()

    try:
        # Run blocking work off the event loop
        result = await run_in_threadpool(handler.handle_event, payload)
        return JSONResponse(status_code=200, content=result)
    except Exception as exc:
        print("INTEGRATION APP ERROR: slack event handling failed:", repr(exc))
        # Slack requires HTTP 200 even on failure
        return JSONResponse(status_code=200, content={"ok": False})
