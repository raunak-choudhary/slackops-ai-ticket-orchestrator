# src/mail_client_adapter/src/mail_client_adapter/adapter.py
"""
Adapter module that connects the service client with the backend logic.

This module acts as a bridge between the Mail Client Service (FastAPI)
and the generated OpenAPI client (mail_client_service_client). It provides
a higher-level abstraction for sending, reading, and managing emails.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Import generated client (robust to monorepo layout during local dev)
# ---------------------------------------------------------------------------
try:
    # Preferred: installed package
    from mail_client_service_client import Client as GeneratedClient  # type: ignore
    from mail_client_service_client.api.messages import (  # type: ignore
        list_messages_messages_get as api_list_messages,
        get_message_messages_message_id_get as api_get_message,
        delete_message_messages_message_id_delete as api_delete_message,
        mark_as_read_messages_message_id_mark_as_read_post as api_mark_as_read,
    )
    logger.debug("Imported generated client from installed package.")
except ModuleNotFoundError:
    # Fallback: add "<repo-root>/clients/python" to sys.path
    here = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(here, "../../../.."))
    clients_python = os.path.join(repo_root, "clients", "python")
    if clients_python not in sys.path:
        sys.path.insert(0, clients_python)
    try:
        from mail_client_service_client import Client as GeneratedClient  # type: ignore
        from mail_client_service_client.api.messages import (  # type: ignore
            list_messages_messages_get as api_list_messages,
            get_message_messages_message_id_get as api_get_message,
            delete_message_messages_message_id_delete as api_delete_message,
            mark_as_read_messages_message_id_mark_as_read_post as api_mark_as_read,
        )
        logger.debug("Imported generated client via monorepo fallback path.")
    except ModuleNotFoundError:  # pragma: no cover
        logger.error(
            "Could not import 'mail_client_service_client'. "
            "Install it (e.g., `uv pip install -e clients/python`) or ensure codegen ran."
        )
        raise


# ---------------------------------------------------------------------------
# Utility: normalize generated objects into dicts/lists
# ---------------------------------------------------------------------------
def _to_plain(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, list):
        return [_to_plain(x) for x in obj]
    if hasattr(obj, "to_dict"):
        try:
            return obj.to_dict()  # type: ignore[attr-defined]
        except Exception:
            return obj
    if isinstance(obj, dict):
        return obj
    return obj


# ---------------------------------------------------------------------------
# Adapter around generated client
# ---------------------------------------------------------------------------
class ServiceAdapter:
    """Wraps the generated Mail Client Service client."""

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self._client = GeneratedClient(base_url=base_url)
        logger.debug("ServiceAdapter initialized with base_url=%s", base_url)

    def list_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        logger.debug("Adapter.list_messages(limit=%s)", limit)
        if limit is None:
            data = api_list_messages.sync(client=self._client)  # type: ignore[attr-defined]
        else:
            data = api_list_messages.sync(client=self._client, limit=limit)  # type: ignore[attr-defined]
        return _to_plain(data) or []

    def get_message(self, message_id: str) -> Dict[str, Any]:
        logger.debug("Adapter.get_message(id=%s)", message_id)
        data = api_get_message.sync(client=self._client, message_id=message_id)  # type: ignore[attr-defined]
        out = _to_plain(data)
        return out if isinstance(out, dict) else {"id": message_id}

    def delete_message(self, message_id: str) -> Dict[str, Any]:
        logger.debug("Adapter.delete_message(id=%s)", message_id)
        data = api_delete_message.sync(client=self._client, message_id=message_id)  # type: ignore[attr-defined]
        out = _to_plain(data)
        if isinstance(out, dict):
            return out
        return {"id": message_id, "deleted": True}

    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        logger.debug("Adapter.mark_as_read(id=%s)", message_id)
        data = api_mark_as_read.sync(client=self._client, message_id=message_id)  # type: ignore[attr-defined]
        out = _to_plain(data)
        if isinstance(out, dict):
            return out
        return {"id": message_id, "status": "read"}


# ---------------------------------------------------------------------------
# Optional higher-level façade (to integrate later with email_api.Client ABC)
# ---------------------------------------------------------------------------
class ServiceBackedClient:
    """Simplified façade over ServiceAdapter."""

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.adapter = ServiceAdapter(base_url=base_url)
        logger.debug("ServiceBackedClient initialized with base_url=%s", base_url)

    def fetch_all_emails(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        return self.adapter.list_messages(limit=limit)

    def fetch_email(self, message_id: str) -> Dict[str, Any]:
        return self.adapter.get_message(message_id)

    def remove_email(self, message_id: str) -> Dict[str, Any]:
        return self.adapter.delete_message(message_id)

    def mark_email_as_read(self, message_id: str) -> Dict[str, Any]:
        return self.adapter.mark_as_read(message_id)