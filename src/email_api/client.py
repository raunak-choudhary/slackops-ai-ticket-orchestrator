"""
email_api.client (package source)
Defines Email and Client used by: `import email_api`
"""

from dataclasses import dataclass


@dataclass
class Email:
    """
    Represents an email message with sender, recipient, subject, and body.

    Defaults allow Email() to be instantiated with no arguments.
    """

    sender: str = ""
    recipient: str = ""
    subject: str = ""
    body: str = ""

    def __str__(self) -> str:
        return f"From: {self.sender}\nTo: {self.recipient}\nSubject: {self.subject}\n\n{self.body}"


class Client:
    """
    A lightweight email API client for basic email operations (in-memory).
    """

    def __init__(self) -> None:
        self._sent_messages: list[Email] = []

    def send_email(self, email: Email) -> bool:
        if not email.sender or not email.recipient:
            raise ValueError("Sender and recipient must be provided.")
        self._sent_messages.append(email)
        return True

    def list_emails(self) -> list[Email]:
        return self._sent_messages

    def get_email(self, index: int) -> Email | None:
        if 0 <= index < len(self._sent_messages):
            return self._sent_messages[index]
        return None

    def delete_email(self, index: int) -> bool:
        if 0 <= index < len(self._sent_messages):
            del self._sent_messages[index]
            return True
        return False
