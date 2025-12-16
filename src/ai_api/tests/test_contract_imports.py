"""Tests for ai_api public contract imports."""

import importlib


def test_can_import_ai_api_package() -> None:
    """ai_api package should be importable."""
    module = importlib.import_module("ai_api")
    assert module is not None


def test_can_import_ai_interface_from_package() -> None:
    """AIInterface should be importable from ai_api."""
    from ai_api import AIInterface  # noqa: F401


def test_can_import_get_client_from_package() -> None:
    """get_client should be importable from ai_api."""
    from ai_api import get_client  # noqa: F401
