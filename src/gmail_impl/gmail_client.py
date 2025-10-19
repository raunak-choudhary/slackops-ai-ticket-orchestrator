"""
Gmail implementation module.
Provides GmailClient and Email class for testing and integration.
"""

from typing import List, Optional
from datetime import datetime


class Email:
    """Represents an email object."""

    def __init__(
        self,
        sender: str = "",
        recipient: str = "",
        subject: str = "",
        body: str = "",
        date: Optional[str] = None,
    ) -> None:
        """Allow both default and parameterized initialization."""
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        return (
            f"<Email from={self.sender} to={self.recipient} "
            f"subject={self.subject}>"
        )


class GmailClient:
    """Simulated Gmail client for sending and fetching emails."""

    def __init__(self) -> None:
        self._inbox: List[Email] = []
        self._sent: List[Email] = []

    def send(self, email: Email) -> str:
        """Simulate sending an email."""
        if not isinstance(email, Email):
            raise TypeError("Expected an Email instance")
        self._sent.append(email)
        return "sent"

    def fetch(self, count: int = 3) -> List[Email]:
        """Simulate fetching emails."""
        # Simulate fixed demo emails for testing
        self._inbox = [
            Email(
                sender="test_sender@example.com",
                recipient="test_recipient@example.com",
                subject="Welcome to OSPSD",
                body="This is your onboarding message.",
            ),
            Email(
                sender="test_sender@example.com",
                recipient="test_recipient@example.com",
                subject="System Update Notice",
                body="System update will occur at midnight.",
            ),
            Email(
                sender="test_sender@example.com",
                recipient="test_recipient@example.com",
                subject="Meeting Reminder: 3 PM",
                body="Don't forget your team sync at 3 PM.",
            ),
        ]
        return self._inbox[:count]

    def list_sent(self) -> List[Email]:
        """Return list of sent emails."""
        return self._sent

    def clear_inbox(self) -> None:
        """Clear the inbox (for test cleanup)."""
        self._inbox.clear()


# Optional demo
if __name__ == "__main__":
    client = GmailClient()
    print("=== Demo: Fetch Emails ===")
    for email in client.fetch():
        print(email)
