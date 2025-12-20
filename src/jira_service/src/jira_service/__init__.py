"""Jira ticket service.

FastAPI service that exposes the OSS Tickets API over HTTP.
The underlying Jira implementation is provided via dependency injection
from the jira_impl package.
"""

from __future__ import annotations
