# src/mail_client_adapter/src/mail_client_adapter/backed_client.py
"""
Compatibility layer for tests that import `mail_client_adapter.backed_client as bc`
and expect `bc.ServiceAdapter` and `bc.AdapterClient` to exist.
"""

from __future__ import annotations

from .adapter import AdapterClient, ServiceAdapter

__all__ = ["AdapterClient", "ServiceAdapter"]
