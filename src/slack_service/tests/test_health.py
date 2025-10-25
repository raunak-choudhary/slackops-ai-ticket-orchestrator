import sys
import os
from fastapi.testclient import TestClient

# Add root folder (where `src` lives) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.slack_service.src.slack_service.app import app


def test_health_ok():
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json().get("status") == "ok"
