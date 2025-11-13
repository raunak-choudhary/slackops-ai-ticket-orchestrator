# src/mail_client_service/tests/conftest.py
from __future__ import annotations

import importlib.util
import sys
import types
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import email_api

# ---------- Paths ----------
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

APP_FILE = ROOT / "src" / "mail_client_service" / "app.py"
SUBMOD_NAME = "mail_client_service.app"
spec = importlib.util.spec_from_file_location(SUBMOD_NAME, APP_FILE)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load spec for {APP_FILE}")
mod = importlib.util.module_from_spec(spec)
assert isinstance(mod, types.ModuleType)
spec.loader.exec_module(mod)  # loader is guaranteed non-None above
if not hasattr(mod, "app"):
    raise ImportError(f"{APP_FILE} loaded as {SUBMOD_NAME}, but no global `app` found.")
app = mod.app  # direct attribute access


# ---------- Fixtures ----------
@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """FastAPI test client."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_mail_client(monkeypatch):
    """Patch email_api.get_client to return a mock client."""
    mock = Mock()
    monkeypatch.setattr(email_api, "get_client", lambda: mock)
    return mock
