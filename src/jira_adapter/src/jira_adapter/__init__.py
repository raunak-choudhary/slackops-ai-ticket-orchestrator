"""Service-backed Jira adapter.

Implements the Tickets API by delegating all operations to the
Jira FastAPI service via the auto-generated HTTP client.
"""

from __future__ import annotations

import os

import tickets_api
from jira_adapter.adapter import JiraServiceTicketClient


def _get_jira_service_client() -> JiraServiceTicketClient:
    """Create and return a Jira service-backed ticket client."""
    return JiraServiceTicketClient(
        base_url=os.environ["JIRA_SERVICE_BASE_URL"],
    )


# Register dependency injection hook (PACKAGE-LEVEL)
tickets_api.get_client = _get_jira_service_client
