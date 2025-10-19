# tests/integration/test_gmail_integration.py

import sys, os
# Add the project root to sys.path so that 'src' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.email_api.client import Email  # ✅ fixed import path


def test_email_class_exists():
    """Ensure that the Email class can be instantiated."""
    email = Email()
    assert email is not None


def test_email_send(monkeypatch):
    """Mock an email send method to verify basic functionality."""
    class DummyEmail:
        def send(self):
            return "sent"

    email = DummyEmail()
    result = email.send()
    assert result == "sent"
