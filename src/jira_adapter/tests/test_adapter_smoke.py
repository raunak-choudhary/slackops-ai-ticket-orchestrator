"""Tests for Jira service-backed adapter."""

from __future__ import annotations

import importlib
from unittest.mock import Mock, patch

import tickets_api
import jira_adapter
from tickets_api.client import TicketStatus


def setup_function() -> None:
    """Reload adapter so DI is re-registered for each test."""
    importlib.reload(jira_adapter)


def test_di_injection_returns_service_client(monkeypatch) -> None:
    """DI should return a Jira service-backed ticket client."""
    monkeypatch.setenv("JIRA_SERVICE_BASE_URL", "http://testserver")

    client = tickets_api.get_client()
    assert client is not None
    assert client.__class__.__name__ == "JiraServiceTicketClient"


def test_get_ticket_transforms_response(monkeypatch) -> None:
    """Adapter should transform TicketOut DTO to domain Ticket."""
    monkeypatch.setenv("JIRA_SERVICE_BASE_URL", "http://testserver")

    mock_dto = Mock()
    mock_dto.id = "T-1"
    mock_dto.title = "Bug"
    mock_dto.description = "Something broke"
    mock_dto.status = "open"
    mock_dto.assignee = None

    with patch(
        "jira_adapter.adapter.get_ticket",
        return_value=mock_dto,
    ):
        client = tickets_api.get_client()
        ticket = client.get_ticket("T-1")

    assert ticket is not None
    assert ticket.id == "T-1"
    assert ticket.title == "Bug"
    assert ticket.status == TicketStatus.OPEN


def test_create_ticket_success(monkeypatch) -> None:
    """create_ticket should return a Ticket domain object."""
    monkeypatch.setenv("JIRA_SERVICE_BASE_URL", "http://testserver")

    mock_dto = Mock()
    mock_dto.id = "T-2"
    mock_dto.title = "New"
    mock_dto.description = "Desc"
    mock_dto.status = "open"
    mock_dto.assignee = None

    with patch(
        "jira_adapter.adapter.create_ticket",
        return_value=mock_dto,
    ):
        client = tickets_api.get_client()
        ticket = client.create_ticket("New", "Desc")

    assert ticket.id == "T-2"
    assert ticket.title == "New"


def test_search_tickets_transforms_list(monkeypatch) -> None:
    """search_tickets should transform list response."""
    monkeypatch.setenv("JIRA_SERVICE_BASE_URL", "http://testserver")

    mock_dto1 = Mock(id="T-1", title="A", description="A", status="open", assignee=None)
    mock_dto2 = Mock(id="T-2", title="B", description="B", status="closed", assignee=None)

    mock_response = Mock()
    mock_response.tickets = [mock_dto1, mock_dto2]

    with patch(
        "jira_adapter.adapter.list_tickets",
        return_value=mock_response,
    ):
        client = tickets_api.get_client()
        tickets = client.search_tickets()

    assert len(tickets) == 2
    assert tickets[0].id == "T-1"
    assert tickets[1].status == TicketStatus.CLOSED


def test_update_ticket_not_supported(monkeypatch) -> None:
    """update_ticket should fail cleanly since service does not support it."""
    monkeypatch.setenv("JIRA_SERVICE_BASE_URL", "http://testserver")

    client = tickets_api.get_client()

    try:
        client.update_ticket("T-1", status=TicketStatus.CLOSED)
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True


def test_delete_ticket_not_supported(monkeypatch) -> None:
    """delete_ticket should fail cleanly since service does not support it."""
    monkeypatch.setenv("JIRA_SERVICE_BASE_URL", "http://testserver")

    client = tickets_api.get_client()

    try:
        client.delete_ticket("T-1")
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True
