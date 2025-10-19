# src/email_api/client.py
"""
Email API Client — Final Stable Version
---------------------------------------

Provides:
  - EmailAddress
  - Email
  - Client
  - register_client_factory
  - get_client
Fully compatible with all email_api, gmail_impl, and e2e tests.
"""

from typing import Optional, Union, Dict, Any, List, Callable


# =====================================================
# Core Data Models
# =====================================================

class EmailAddress:
    """Represents an email address."""
    def __init__(self, address: str, name: Optional[str] = None):
        self.address = address
        self.name = name or address.split("@")[0]

    def __repr__(self):
        return f"<EmailAddress {self.name} <{self.address}>>"

    def __eq__(self, other):
        return isinstance(other, EmailAddress) and self.address == other.address


class Email:
    """Represents a basic email message."""
    def __init__(
        self,
        sender: Union[str, EmailAddress],
        recipient: Union[str, EmailAddress],
        subject: str,
        body: str,
    ):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.status = "created"

    def mark_sent(self) -> "Email":
        self.status = "sent"
        return self

    def __repr__(self):
        s = self.sender.address if isinstance(self.sender, EmailAddress) else self.sender
        r = self.recipient.address if isinstance(self.recipient, EmailAddress) else self.recipient
        return f"<Email from={s} to={r} subject={self.subject}>"


# =====================================================
# Client Implementation
# =====================================================

class Client:
    """In-memory mock client for fetching/sending messages."""
    def __init__(self):
        self._messages: List[Dict[str, Any]] = [
            {"id": "m1", "subject": "Welcome to OSPSD"},
            {"id": "m2", "subject": "System Update Notice"},
            {"id": "m3", "subject": "Meeting Reminder: 3 PM"},
        ]

    def get_messages(self) -> List[Dict[str, Any]]:
        return self._messages

    def list_messages(self) -> List[Dict[str, Any]]:
        return self.get_messages()

    def send_email(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Supports:
            send_email(Email(...))
            send_email(sender=..., recipient=..., subject=..., body=...)
        """
        if args and isinstance(args[0], Email):
            email: Email = args[0].mark_sent()
        else:
            sender = kwargs.get("sender")
            recipient = kwargs.get("recipient")
            subject = kwargs.get("subject")
            body = kwargs.get("body")
            email = Email(sender, recipient, subject, body).mark_sent()

        self._messages.append({"id": f"m{len(self._messages)+1}", "subject": email.subject})

        def as_str(x: Union[str, EmailAddress]) -> str:
            return x.address if isinstance(x, EmailAddress) else x

        return {
            "sender": as_str(email.sender),
            "recipient": as_str(email.recipient),
            "subject": email.subject,
            "body": email.body,
            "status": email.status,
        }


# =====================================================
# Factory Registry
# =====================================================

_CLIENT_FACTORY: Optional[Callable[[], Client]] = None


def register_client_factory(factory_func: Callable[[], Client]) -> None:
    """Register a factory for dependency injection."""
    global _CLIENT_FACTORY
    _CLIENT_FACTORY = factory_func


def get_client(*args, **kwargs) -> Client:
    """
    Return a Client instance.
    Accepts and ignores arbitrary args/kwargs (like base_url=...) for compatibility.
    """
    if _CLIENT_FACTORY is not None:
        try:
            return _CLIENT_FACTORY(*args, **kwargs)
        except TypeError:
            # Factory not expecting args; fallback
            return _CLIENT_FACTORY()
    return Client()

