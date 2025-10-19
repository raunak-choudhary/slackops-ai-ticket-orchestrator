# src/mail_client_adapter/src/mail_client_adapter/adapter.py

"""
Adapter module that connects the service client with the backend logic.

This module acts as a bridge between the Mail Client Service (FastAPI)
and the generated client (mail_client_service_client). It provides
a higher-level abstraction for sending, reading, and managing emails.
"""

from __future__ import annotations

import logging
from typing import List, Dict, Any, Optional

# ✅ Fixed import path
# Previously: from mail_client_service_client import Client as GeneratedClient
from src.mail_client_service_client import Client as GeneratedClient


logger = logging.getLogger(__name__)


class ServiceAdapter:
    """
    High-level adapter that wraps around the generated Mail Client Service client.
    Provides simplified methods for interacting with the mail service API.
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.client = GeneratedClient(base_url=base_url)
        logger.debug("ServiceAdapter initialized with base_url=%s", base_url)

    def list_messages(self) -> List[Dict[str, Any]]:
        """Fetches all messages."""
        logger.debug("Fetching all messages from mail client service")
        response = self.client.messages.list_messages_messages_get.sync()
        logger.debug("Received response: %s", response)
        return response or []

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """Fetches a single message by ID."""
        logger.debug("Fetching message with ID: %s", message_id)
        response = self.client.messages.get_message_messages_message_id_get.sync(message_id=message_id)
        logger.debug("Received message: %s", response)
        return response

    def delete_message(self, message_id: str) -> bool:
        """Deletes a message."""
        logger.debug("Deleting message with ID: %s", message_id)
        response = self.client.messages.delete_message_messages_message_id_delete.sync(message_id=message_id)
        logger.debug("Delete response: %s", response)
        return response is not None

    def mark_as_read(self, message_id: str) -> bool:
        """Marks a message as read."""
        logger.debug("Marking message as read: %s", message_id)
        response = self.client.messages.mark_as_read_messages_message_id_mark_as_read_post.sync(
            message_id=message_id
        )
        logger.debug("Mark-as-read response: %s", response)
        return response is not None


class ServiceBackedClient:
    """
    Client wrapper that uses the ServiceAdapter to perform mail operations.
    Acts as the local interface for application logic or API endpoints.
    """

    def __init__(self, adapter: Optional[ServiceAdapter] = None) -> None:
        self.adapter = adapter or ServiceAdapter()
        logger.debug("ServiceBackedClient initialized")

    def fetch_all_emails(self) -> List[Dict[str, Any]]:
        logger.debug("Fetching all emails via ServiceBackedClient")
        return self.adapter.list_messages()

    def fetch_email(self, message_id: str) -> Dict[str, Any]:
        logger.debug("Fetching single email via ServiceBackedClient, ID=%s", message_id)
        return self.adapter.get_message(message_id)

    def remove_email(self, message_id: str) -> bool:
        logger.debug("Deleting email via ServiceBackedClient, ID=%s", message_id)
        return self.adapter.delete_message(message_id)

    def mark_email_as_read(self, message_id: str) -> bool:
        logger.debug("Marking email as read via ServiceBackedClient, ID=%s", message_id)
        return self.adapter.mark_as_read(message_id)
