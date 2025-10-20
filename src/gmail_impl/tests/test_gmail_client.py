# src/gmail_impl/tests/test_gmail_client.py
from __future__ import annotations

import sys
from pathlib import Path

# Ensure that the 'src' directory is in Python path
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import pytest  # noqa: E402

from email_api.client import Email  # noqa: E402
from gmail_impl.gmail_client import GmailClient  # noqa: E402


@pytest.fixture
def dummy_email():
    return Email(
        sender="test_sender@example.com",
        recipient="test_recipient@example.com",
        subject="Test Subject",
        body="This is a test email body.",
    )


def test_gmail_client_send(monkeypatch, dummy_email):
    """Mock GmailClient send method to simulate sending."""
    client = GmailClient()

    def mock_send(email):
        assert email.subject == "Test Subject"
        return "sent"

    monkeypatch.setattr(client, "send", mock_send)
    result = client.send(dummy_email)
    assert result == "sent"


def test_gmail_client_fetch(monkeypatch):
    """Mock GmailClient fetch method to simulate message retrieval."""
    client = GmailClient()

    def mock_fetch():
        return [{"id": "123", "subject": "Hello"}]

    monkeypatch.setattr(client, "fetch", mock_fetch)
    messages = client.fetch()
    assert isinstance(messages, list)
    assert messages[0]["subject"] == "Hello"