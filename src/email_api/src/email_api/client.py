"""
Email API client module.
Defines the Email class and a simple EmailApiClient for testing and integration.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Email:
    """Represents a basic email message."""
    sender: str = ""
    recipient: str = ""
    subject: str = ""
    body: str = ""


class EmailApiClient:
    """A simple simulated email API client."""

    def __init__(self) -> None:
        self._messages: List[Email] = [
            Email(
                sender="test_sender@example.com",
                recipient="test_recipient@example.com",
                subject="Welcome to OSPSD",
                body="This is a test email from the Email API.",
            ),
            Email(
                sender="alerts@example.com",
                recipient="user@example.com",
                subject="System Alert",
                body="Your account activity has been updated.",
            ),
        ]

    def get_messages(self) -> List[Email]:
        """Simulate fetching a list of email messages."""
        return self._messages

    def add_message(self, email: Email) -> None:
        """Add a message to the simulated store."""
        if not isinstance(email, Email):
            raise TypeError("Expected an Email instance")
        self._messages.append(email)

    def clear_messages(self) -> None:
        """Clear all stored emails."""
        self._messages.clear()


# Optional standalone run
if __name__ == "__main__":
    client = EmailApiClient()
    print("=== Demo: Email API ===")
    for msg in client.get_messages():
        print(f"From: {msg.sender}, Subject: {msg.subject}")
