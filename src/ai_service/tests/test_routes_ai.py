from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from ai_service.main import create_app


class _FakeAIClient:
    def generate_response(
        self,
        user_input: str,
        system_prompt: str,
        response_schema: dict[str, object] | None = None,
    ) -> str | dict[str, object]:
        if response_schema:
            return {"intent": "NO_ACTION"}
        return "hello"


def test_health_endpoint() -> None:
    """Health endpoint returns healthy status."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_generate_conversational() -> None:
    """Conversational generation returns string."""
    app = create_app()

    with patch("ai_service.routes.get_client", return_value=_FakeAIClient()):
        client = TestClient(app)

        response = client.post(
            "/generate",
            json={
                "user_input": "hi",
                "system_prompt": "be helpful",
            },
        )

    assert response.status_code == 200
    assert response.json() == {"result": "hello"}


def test_generate_structured() -> None:
    """Structured generation returns dict."""
    app = create_app()

    with patch("ai_service.routes.get_client", return_value=_FakeAIClient()):
        client = TestClient(app)

        response = client.post(
            "/generate",
            json={
                "user_input": "hello",
                "system_prompt": "extract intent",
                "response_schema": {
                    "name": "intent",
                    "schema": {"type": "object"},
                },
            },
        )

    assert response.status_code == 200
    assert response.json() == {"result": {"intent": "NO_ACTION"}}


def test_generate_failure_is_sanitized() -> None:
    """Provider failures must not leak internals."""
    app = create_app()

    class _FailingClient:
        def generate_response(self, *args: object, **kwargs: object) -> str:
            raise RuntimeError("boom")

    with patch("ai_service.routes.get_client", return_value=_FailingClient()):
        client = TestClient(app)

        response = client.post(
            "/generate",
            json={
                "user_input": "hi",
                "system_prompt": "be helpful",
            },
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "AI service failed to generate a response"
