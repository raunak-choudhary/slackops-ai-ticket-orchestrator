"""
Stub GmailClient class for structural integrity tests.
This is *not* the production Gmail client.
"""

from __future__ import annotations


class GmailClient:
    def __init__(self) -> None:
        self._sent: list[str] = []

    def send(self, _email=None):
        # Signature kept for compatibility; argument intentionally unused.
        self._sent.append("sent")
        return "sent"
