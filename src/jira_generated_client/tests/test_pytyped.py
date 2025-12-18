"""Typing marker test."""

import importlib.resources


def test_pytyped_exists() -> None:
    """py.typed marker must exist for PEP 561 compliance."""
    assert importlib.resources.is_resource(
        "tickets_service_api_client",
        "py.typed",
    )
