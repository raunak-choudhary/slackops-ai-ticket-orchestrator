# src/jira_impl/src/jira_impl/config.py
"""Runtime configuration for Jira-backed ticketing (env-driven only)."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JiraConfig:
    """Configuration for Jira Cloud REST API (API token auth)."""

    base_url: str
    email: str
    api_token: str
    project_key: str

    @staticmethod
    def from_env() -> "JiraConfig":
        """Load Jira settings from environment variables.

        Required:
          - JIRA_BASE_URL       e.g. https://your-domain.atlassian.net
          - JIRA_EMAIL          Atlassian account email
          - JIRA_API_TOKEN      Atlassian API token
          - JIRA_PROJECT_KEY    Jira project key (e.g., "PROJ")

        Raises:
            RuntimeError: If any required environment variable is missing.
        """
        base_url = os.environ.get("JIRA_BASE_URL", "").strip().rstrip("/")
        email = os.environ.get("JIRA_EMAIL", "").strip()
        api_token = os.environ.get("JIRA_API_TOKEN", "").strip()
        project_key = os.environ.get("JIRA_PROJECT_KEY", "").strip()

        missing: list[str] = []
        if not base_url:
            missing.append("JIRA_BASE_URL")
        if not email:
            missing.append("JIRA_EMAIL")
        if not api_token:
            missing.append("JIRA_API_TOKEN")
        if not project_key:
            missing.append("JIRA_PROJECT_KEY")

        if missing:
            raise RuntimeError(f"Missing required Jira environment variables: {', '.join(missing)}")

        return JiraConfig(
            base_url=base_url,
            email=email,
            api_token=api_token,
            project_key=project_key,
        )
