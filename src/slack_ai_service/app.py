from fastapi import FastAPI
from slack_ai_service.routes.ai import router as ai_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Slack AI Service Running"}

app.include_router(ai_router)
