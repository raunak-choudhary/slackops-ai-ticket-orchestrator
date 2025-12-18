"""
Unit tests for jira_impl.jira_client.

These tests mock httpx.Client (used as a context manager) to exercise
success, error, and exception paths without making real HTTP calls.
No production code is modified.
"""

from unittest.mock import Mock, patch

import pytest
import httpx

from jira_impl.jira_client import JiraClient


@pytest.mark.unit
def test_jira_client_initializes_successfully() -> None:
    """JiraClient can be constructed with valid parameters."""
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    assert client is not None


@pytest.mark.unit
def test_jira_client_request_success_response() -> None:
    """_request returns response object on HTTP 200."""
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "TEST-123"}

    mock_client = Mock()
    mock_client.request.return_value = mock_response

    with patch("jira_impl.jira_client.httpx.Client") as client_cls:
        client_cls.return_value.__enter__.return_value = mock_client

        resp = client._request("GET", "/rest/api/3/issue/TEST-123")

    assert resp.status_code == 200
    assert resp.json()["key"] == "TEST-123"


@pytest.mark.unit
def test_jira_client_request_non_200_response() -> None:
    """_request returns response even for non-200 status codes."""
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_client = Mock()
    mock_client.request.return_value = mock_response

    with patch("jira_impl.jira_client.httpx.Client") as client_cls:
        client_cls.return_value.__enter__.return_value = mock_client

        resp = client._request("GET", "/rest/api/3/issue/FAIL")

    assert resp.status_code == 401


@pytest.mark.unit
def test_jira_client_request_raises_connection_error_on_httpx_exception() -> None:
    """httpx.RequestError is translated into ConnectionError."""
    client = JiraClient(
        base_url="https://example.atlassian.net",
        email="user@example.com",
        api_token="fake-token",
    )

    mock_client = Mock()
    mock_client.request.side_effect = httpx.RequestError("boom")

    with patch("jira_impl.jira_client.httpx.Client") as client_cls:
        client_cls.return_value.__enter__.return_value = mock_client

        with pytest.raises(ConnectionError):
            client._request("GET", "/rest/api/3/issue/ERROR")
