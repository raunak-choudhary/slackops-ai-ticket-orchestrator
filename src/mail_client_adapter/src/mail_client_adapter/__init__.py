# src/mail_client_adapter/src/mail_client_adapter/__init__.py
"""
mail_client_adapter package

Exports:
    - AdapterClient: shim implementing email_api.Client interface
    - ServiceAdapter: concrete adapter around generated service client
    - ServiceBackedClient: simple façade used in unit tests
"""

from __future__ import annotations

from .adapter import AdapterClient, ServiceAdapter, ServiceBackedClient

__all__ = ["AdapterClient", "ServiceAdapter", "ServiceBackedClient"]