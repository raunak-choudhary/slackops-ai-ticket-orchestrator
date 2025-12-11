from fastapi import APIRouter
import os
import requests
from slack_ai_service.models import AIRequest

router = APIRouter(prefix="/ai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

@router.post("/generate")
def generate_text(data: AIRequest):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": data.prompt}
        ]
    }

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body
    )

    if resp.status_code != 200:
        return {"error": resp.text}

    result = resp.json()
    output = result["choices"][0]["message"]["content"]

    return {"response": output}
