# src/mail_client_adapter/src/mail_client_adapter/mapping.py
"""
Mapping utilities for converting service or adapter payloads
into the canonical Email model defined in email_api.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from email_api import Email


def to_email(raw: Mapping[str, Any]) -> Email:
    """
    Convert a dict-like object returned by the service/adapter
    into an Email instance. The email_api.Email here requires
    `sender` and `subject` (both strings).
    """
    sender = str(raw.get("sender", ""))
    subject = str(raw.get("subject", ""))
    return Email(sender=sender, subject=subject)