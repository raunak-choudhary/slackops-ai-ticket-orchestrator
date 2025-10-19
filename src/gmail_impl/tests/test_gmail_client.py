# src/gmail_impl/tests/test_gmail_client.py

import sys
import os
# Ensure that the 'src' directory is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
from src.email_api.client import Email  # ✅ Fixed import (was 'from email_api import Email')
from src.gmail_impl.gmail_client import GmailClient  # Assuming this class exists in gmail_client.py


@pytest.fixture
def dummy_email():
    """Fixture to create a dummy Email instance."""
    email = Email(
        sender="test_sender@example.com",
        recipient="test_recipient@example.com",
        subject="Test Subject",
        body="This is a test email body."
    )
    return email


def test_email_initialization(dummy_email):
    """Ensure Email class initializes correctly."""
    assert dummy_email.sender == "test_sender@example.com"
    assert dummy_email.recipient == "test_recipient@example.com"
    assert dummy_email.subject == "Test Subject"


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
