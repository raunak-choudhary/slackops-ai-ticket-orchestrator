# src/email_api/tests/test_api.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
from src.email_api.client import Client


class MockClient(Client):
    """Concrete mock subclass of the abstract Client for testing."""
    def get_messages(self):
        return [{"id": "1", "subject": "Mock message"}]


def test_client_initialization():
    """Test that the abstract Client can be subclassed and instantiated."""
    client = MockClient()
    assert client is not None


def test_get_messages_returns_list():
    """Test that get_messages returns a list of messages."""
    client = MockClient()
    messages = client.get_messages()
    assert isinstance(messages, list)
    assert messages[0]["subject"] == "Mock message"
