# src/jira_impl/tests/test_env_vars.py
"""Environment variable tests for JiraConfig."""

from __future__ import annotations

import pytest

from jira_impl.config import JiraConfig


def test_config_requires_all_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    """Missing required env vars should raise a RuntimeError."""
    for key in ["JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"]:
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(RuntimeError):
        JiraConfig.from_env()


def test_config_reads_and_trims(monkeypatch: pytest.MonkeyPatch) -> None:
    """Values should be read from env, trimmed, and base_url normalized."""
    monkeypatch.setenv("JIRA_BASE_URL", " https://example.atlassian.net/ ")
    monkeypatch.setenv("JIRA_EMAIL", " user@example.com ")
    monkeypatch.setenv("JIRA_API_TOKEN", " token ")
    monkeypatch.setenv("JIRA_PROJECT_KEY", " PROJ ")

    cfg = JiraConfig.from_env()
    assert cfg.base_url == "https://example.atlassian.net"
    assert cfg.email == "user@example.com"
    assert cfg.api_token == "token"
    assert cfg.project_key == "PROJ"
