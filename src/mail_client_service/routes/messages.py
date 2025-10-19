from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

# Tests monkeypatch email_api.get_client in their conftest.py
import email_api

router = APIRouter()


def get_mail_client():
    """Obtain a client each request so the tests' monkeypatch applies."""
    return email_api.get_client()


def _exc_to_status(exc: Exception) -> int:
    """Map known error types by name (no assumptions about module paths)."""
    name = type(exc).__name__
    if "NotFound" in name:
        return status.HTTP_404_NOT_FOUND
    if "BadRequest" in name:
        return status.HTTP_400_BAD_REQUEST
    if "Validation" in name:
        return status.HTTP_422_UNPROCESSABLE_ENTITY
    return status.HTTP_500_INTERNAL_SERVER_ERROR


@router.get("", response_model=list[Any])
def list_messages(
    limit: Optional[int] = Query(default=None, ge=1),
    client=Depends(get_mail_client),
) -> list[Any]:
    """
    Return a list of message summaries.
    - routes tests: ensure list and shape
    - service tests: use DummyClient with fixed payload
    """
    try:
        if limit is not None:
            return client.list_messages(limit=limit)
        return client.list_messages()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=_exc_to_status(exc), detail=str(exc)) from exc


@router.get("/{message_id}")
def get_message(
    message_id: str,
    client=Depends(get_mail_client),
) -> Any:
    """Return a full message by ID."""
    try:
        return client.get_message(message_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=_exc_to_status(exc), detail=str(exc)) from exc


@router.post("/{message_id}/mark-as-read")
def mark_as_read(
    message_id: str,
    client=Depends(get_mail_client),
) -> Any:
    """
    Mark a message as read.
    - routes tests: mock returns {"id": "m_123", "is_read": True} and they check ["is_read"]
    - service tests: DummyClient returns {"id": "...", "status": "read"} and they check equality
    Therefore: return the client's payload verbatim.
    """
    try:
        return client.mark_as_read(message_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=_exc_to_status(exc), detail=str(exc)) from exc


@router.delete("/{message_id}")
def delete_message(
    message_id: str,
    client=Depends(get_mail_client),
) -> Any:
    """
    Delete a message.
    - routes tests: mock returns {"ok": True} and they check ["ok"]
    - service tests: DummyClient returns {"id": "...", "deleted": True"} and they check equality
    Therefore: return the client's payload verbatim.
    """
    try:
        return client.delete_message(message_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=_exc_to_status(exc), detail=str(exc)) from exc