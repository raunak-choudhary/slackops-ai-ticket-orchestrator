"""
Additional unit tests for jira_impl.jira_client methods.

These tests exercise higher-level JiraClient methods while mocking
the underlying HTTP transport. No production code is modified.
"""

from unittest.mock import Mock, patch

import pytest
import httpx

from jira_impl.jira_client import JiraClient, JiraIssue


@pytest.mark.unit
def test_get_issue_success() -> None:
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    response_data = {
        "key": "TEST-1",
        "fields": {
            "summary": "Test summary",
            "description": {"content": [{"content": [{"text": "desc"}]}]},
            "status": {"name": "Open"},
            "assignee": {"accountId": "acc-123"},
        },
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = response_data

    with patch.object(client, "_request", return_value=mock_response):
        issue = client.get_issue("TEST-1")

    assert isinstance(issue, JiraIssue)
    assert issue.key == "TEST-1"
    assert issue.summary == "Test summary"
    assert issue.description == "desc"
    assert issue.status_name == "Open"
    assert issue.assignee_account_id == "acc-123"


@pytest.mark.unit
def test_get_issue_not_found() -> None:
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    mock_response = Mock()
    mock_response.status_code = 404

    with patch.object(client, "_request", return_value=mock_response):
        with pytest.raises(KeyError):
            client.get_issue("MISSING-1")


@pytest.mark.unit
def test_create_issue_success() -> None:
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    create_resp = Mock()
    create_resp.status_code = 201
    create_resp.json.return_value = {"key": "NEW-1"}

    get_resp = Mock()
    get_resp.status_code = 200
    get_resp.json.return_value = {
        "key": "NEW-1",
        "fields": {
            "summary": "Created",
            "description": {"content": []},
            "status": {"name": "Open"},
            "assignee": None,
        },
    }

    with patch.object(client, "_request", side_effect=[create_resp, get_resp]):
        issue = client.create_issue(
            project_key="TEST",
            summary="Created",
            description="desc",
            assignee_account_id=None,
        )

    assert issue.key == "NEW-1"
    assert issue.summary == "Created"


@pytest.mark.unit
def test_delete_issue_success_and_not_found() -> None:
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    ok_resp = Mock()
    ok_resp.status_code = 204

    not_found_resp = Mock()
    not_found_resp.status_code = 404

    with patch.object(client, "_request", return_value=ok_resp):
        assert client.delete_issue("DEL-1") is True

    with patch.object(client, "_request", return_value=not_found_resp):
        assert client.delete_issue("DEL-2") is False
