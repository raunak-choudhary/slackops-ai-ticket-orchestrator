from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool

from integration_app.slack_entry import SlackEventHandler

app = FastAPI(title="HW3 Integration App")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/slack/events")
async def slack_events(request: Request) -> JSONResponse:
    payload = await request.json()

    # 🔒 Slack URL verification MUST return immediately
    if payload.get("type") == "url_verification":
        return JSONResponse(
            status_code=200,
            content={"challenge": payload["challenge"]},
        )

    handler = SlackEventHandler()

    try:
        # Run blocking Slack calls off the event loop
        result = await run_in_threadpool(handler.handle_event, payload)
        return JSONResponse(status_code=200, content=result)
    except Exception:
        # Slack requires HTTP 200 even on failure
        return JSONResponse(status_code=200, content={"ok": False})
