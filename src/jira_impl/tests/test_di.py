"""Dependency injection tests for jira_impl."""

from __future__ import annotations

from tickets_api import client as tickets_api_client


def test_importing_jira_impl_registers_dependency_injection() -> None:
    """Importing jira_impl should register a Jira-backed get_client hook."""
    import jira_impl  # noqa: F401

    # Do NOT call get_client(); constructor requires real env vars.
    get_client = tickets_api_client.get_client

    assert callable(get_client)
    assert get_client.__name__ == "_get_jira_client"
