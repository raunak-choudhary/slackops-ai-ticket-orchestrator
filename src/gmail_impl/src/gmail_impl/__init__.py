"""
gmail_impl package initializer.
Provides access to the GmailClient class for tests and service imports.
"""

from src.gmail_impl.gmail_client import GmailClient  # ✅ correct and stable import

__all__ = ["GmailClient"]
