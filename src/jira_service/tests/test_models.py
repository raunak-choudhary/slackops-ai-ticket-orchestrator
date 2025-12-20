from __future__ import annotations

from tickets_api.client import TicketStatus

from jira_service.models import TicketIn, TicketOut, TicketUpdateIn


def test_models_round_trip() -> None:
    payload = TicketIn(title="T", description="D", assignee=None)
    assert payload.title == "T"

    update = TicketUpdateIn(status=TicketStatus.OPEN, title="New")
    assert update.status == TicketStatus.OPEN

    out = TicketOut(id="X-1", title="T", description="D", status=TicketStatus.OPEN, assignee=None)
    assert out.id == "X-1"
