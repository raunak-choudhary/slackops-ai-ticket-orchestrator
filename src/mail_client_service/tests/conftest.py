# src/mail_client_service/tests/conftest.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from typing import Generator
import pathlib
import sys
import types
import importlib.util
import pytest
from fastapi.testclient import TestClient

# ---------- Paths ----------
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]

# Adjusted paths for both service and email_api
SERVICE_SRC_ROOT = REPO_ROOT / "src" / "mail_client_service"
SERVICE_PKG_DIR = SERVICE_SRC_ROOT
APP_FILE = SERVICE_PKG_DIR / "app.py"

EMAIL_API_SRC_ROOT = REPO_ROOT / "src" / "email_api" / "src"
EMAIL_API_PKG_DIR = EMAIL_API_SRC_ROOT / "email_api"

# Ensure both are importable for runtime imports
for p in (SERVICE_SRC_ROOT, EMAIL_API_SRC_ROOT, EMAIL_API_PKG_DIR):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

# ---------- Stub gmail_impl ----------
if "gmail_impl" not in sys.modules:
    sys.modules["gmail_impl"] = types.ModuleType("gmail_impl")

# ---------- Load app.py ----------
if not APP_FILE.exists():
    raise ImportError(f"app.py not found at expected path: {APP_FILE}")

PKG_NAME = "mail_client_service"
if PKG_NAME not in sys.modules:
    pkg = types.ModuleType(PKG_NAME)
    pkg.__path__ = [str(SERVICE_PKG_DIR)]
    sys.modules[PKG_NAME] = pkg

SUBMOD_NAME = "mail_client_service.app"
spec = importlib.util.spec_from_file_location(
    SUBMOD_NAME, APP_FILE, submodule_search_locations=[str(SERVICE_PKG_DIR)]
)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not create spec for {SUBMOD_NAME} at {APP_FILE}")

mod = importlib.util.module_from_spec(spec)
sys.modules[SUBMOD_NAME] = mod
spec.loader.exec_module(mod)  # type: ignore[attr-defined]

if not hasattr(mod, "app"):
    raise ImportError(f"{APP_FILE} loaded as {SUBMOD_NAME}, but no global `app` found.")
app = getattr(mod, "app")

# ---------- Fixtures ----------
@pytest.fixture()
def test_client() -> Generator[TestClient, None, None]:
    """FastAPI test client."""
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture()
def mock_mail_client(monkeypatch):
    """Patch email_api.get_client to return a mock client."""
    from unittest.mock import Mock
    import email_api

    mock = Mock()
    mock.list_messages.return_value = [
        {
            "id": "m_123",
            "sender": {"address": "alice@example.com"},
            "subject": "Hello",
            "snippet": "Preview…",
            "is_read": False,
        }
    ]
    mock.get_messages.return_value = mock.list_messages.return_value
    mock.get_message.return_value = {
        "id": "m_123",
        "sender": {"address": "alice@example.com"},
        "subject": "Hello",
        "body": "Long body",
        "is_read": False,
    }
    mock.mark_as_read.return_value = {"id": "m_123", "is_read": True}
    mock.delete_message.return_value = {"ok": True}

    monkeypatch.setattr(email_api, "get_client", lambda: mock)
    return mock
