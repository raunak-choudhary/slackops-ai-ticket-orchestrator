from __future__ import annotations

import tickets_api.client as tickets_api_client
from fastapi.testclient import TestClient
from tickets_api.client import Ticket, TicketInterface, TicketStatus

from jira_service.main import app


class _DummyTicket(Ticket):
    def __init__(self, ticket_id: str) -> None:
        self._id = ticket_id

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return "title"

    @property
    def description(self) -> str:
        return "desc"

    @property
    def status(self) -> TicketStatus:
        return TicketStatus.OPEN

    @property
    def assignee(self) -> str | None:
        return None


class _DummyClient(TicketInterface):
    def create_ticket(self, title: str, description: str, assignee: str | None = None) -> Ticket:
        _ = (title, description, assignee)
        return _DummyTicket("PROJ-1")

    def get_ticket(self, ticket_id: str) -> Ticket | None:
        if ticket_id == "MISSING":
            return None
        return _DummyTicket(ticket_id)

    def search_tickets(self, query: str | None = None, status: TicketStatus | None = None) -> list[Ticket]:
        _ = (query, status)
        return [_DummyTicket("PROJ-1"), _DummyTicket("PROJ-2")]

    def update_ticket(self, ticket_id: str, status: TicketStatus | None = None, title: str | None = None) -> Ticket:
        _ = (status, title)
        return _DummyTicket(ticket_id)

    def delete_ticket(self, ticket_id: str) -> bool:
        return ticket_id != "NOPE"


def test_routes_with_injected_dummy_client(monkeypatch) -> None:
    monkeypatch.setattr(tickets_api_client, "get_client", lambda: _DummyClient())

    client = TestClient(app)

    r = client.post("/tickets", json={"title": "A", "description": "B", "assignee": None})
    assert r.status_code == 201
    assert r.json()["id"] == "PROJ-1"

    r = client.get("/tickets/PROJ-9")
    assert r.status_code == 200
    assert r.json()["id"] == "PROJ-9"

    r = client.get("/tickets/MISSING")
    assert r.status_code == 404

    r = client.get("/tickets")
    assert r.status_code == 200
    assert len(r.json()["tickets"]) == 2

    r = client.put("/tickets/PROJ-7", json={"status": "open", "title": "New"})
    assert r.status_code == 200
    assert r.json()["id"] == "PROJ-7"

    r = client.delete("/tickets/NOPE")
    assert r.status_code == 200
    assert r.json()["deleted"] is False
