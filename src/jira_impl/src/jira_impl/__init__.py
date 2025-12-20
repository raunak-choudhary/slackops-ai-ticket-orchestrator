# src/jira_impl/src/jira_impl/__init__.py
"""Jira-backed implementation wiring for the Tickets API.

Importing this package activates dependency injection by registering the
Jira-backed TicketInterface implementation with tickets_api.get_client().
"""

from __future__ import annotations

from tickets_api import client as tickets_api_client

from jira_impl.impl import JiraTicketClient


def _get_jira_client() -> JiraTicketClient:
    """Create and return a Jira-backed ticket client."""
    return JiraTicketClient()


# Monkey-patch the Tickets API dependency injection hook
tickets_api_client.get_client = _get_jira_client
