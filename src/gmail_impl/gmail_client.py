"""
Stub GmailClient class for structural integrity tests.
This is *not* the production Gmail client.
"""

class GmailClient:
    def __init__(self):
        self._messages = [
            {"id": "m1", "subject": "Welcome!", "body": "Thanks for joining!"},
            {"id": "m2", "subject": "Update", "body": "System update notice."},
        ]

    def send(self, email=None):
        return "sent"

    def fetch(self):
        return self._messages
