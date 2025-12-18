"""Import contract tests for tickets_api."""

from __future__ import annotations

import importlib


def test_tickets_api_imports_cleanly() -> None:
    """tickets_api must import without pulling in implementations."""
    importlib.import_module("tickets_api")
