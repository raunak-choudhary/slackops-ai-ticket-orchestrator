"""Smoke tests for generated Client construction."""

from tickets_service_api_client import Client


def test_client_can_be_constructed() -> None:
    """Client should be constructible with a base URL."""
    client = Client(base_url="http://example.com")
    assert client is not None
