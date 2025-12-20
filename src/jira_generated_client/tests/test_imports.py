"""Smoke tests for jira generated client imports."""

from tickets_service_api_client import Client, AuthenticatedClient


def test_client_imports() -> None:
    """Client and AuthenticatedClient should be importable."""
    assert Client is not None
    assert AuthenticatedClient is not None
