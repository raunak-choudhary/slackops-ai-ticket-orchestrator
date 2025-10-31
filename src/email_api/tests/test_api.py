# src/email_api/tests/test_api.py
from __future__ import annotations

import sys
from pathlib import Path

# Put repo root on sys.path
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from email_api.client import Client  # noqa: E402


class MockClient(Client):
    """Concrete mock subclass of Client for testing."""

    def get_messages(self):
        return [{"id": "1", "subject": "Mock message"}]


def test_client_initialization():
    """Test that the Client can be subclassed and instantiated."""
    client = MockClient()
    assert client is not None


def test_get_messages_returns_list():
    """Test that get_messages returns a list of messages."""
    client = MockClient()
    messages = client.get_messages()
    assert isinstance(messages, list)
    assert messages[0]["subject"] == "Mock message"
