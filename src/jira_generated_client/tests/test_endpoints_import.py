"""Smoke tests for generated endpoint functions."""

from tickets_service_api_client.api.default.create_ticket_tickets_post import sync as create_ticket
from tickets_service_api_client.api.default.get_ticket_tickets_ticket_id_get import sync as get_ticket
from tickets_service_api_client.api.default.list_tickets_tickets_get import sync as list_tickets
from tickets_service_api_client.api.default.health_check_health_get import sync as health_check


def test_endpoint_functions_importable() -> None:
    """Generated endpoint functions should be importable."""
    assert create_ticket is not None
    assert get_ticket is not None
    assert list_tickets is not None
    assert health_check is not None
