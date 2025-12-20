"""
Smoke tests for the auto-generated AI service client.

These tests intentionally avoid network calls.
They only verify that:
- The generated client can be imported
- Core symbols exist
- Basic client construction works

This ensures the OpenAPI generation step is valid.
"""

from __future__ import annotations

from ai_service_api_client.ai_service_client import Client
from ai_service_api_client.ai_service_client.api.default import (
    generate_ai_response_ai_generate_post,
)
from ai_service_api_client.ai_service_client.models.ai_request import AIRequest


def test_generated_client_imports() -> None:
    """Generated client modules should be importable."""
    assert Client is not None
    assert generate_ai_response_ai_generate_post is not None
    assert AIRequest is not None


def test_generated_client_can_be_constructed() -> None:
    """Client can be constructed with a base URL."""
    client = Client(base_url="http://example.com")
    assert client is not None
