"""Message endpoints for the mail client service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, cast
from fastapi import APIRouter, HTTPException
import email_api
from email_api import Client

if TYPE_CHECKING:
    from collections.abc import Callable

router = APIRouter(prefix="/messages", tags=["messages"])


def _client() -> Client:
    """Return the injected email client (configured via dependency injection)."""
    return email_api.get_client()


def _require_method(client: Client, name: str) -> Callable[..., object]:
    """Return a callable method from the client or raise 501 if missing."""
    fn = getattr(cast("Any", client), name, None)
    if callable(fn):
        return cast("Callable[..., object]", fn)
    raise HTTPException(
        status_code=501,
        detail=f"{name} is not implemented by email_api.Client",
    )


# ---------------------------------------------------------------------------
# LIST MESSAGES ENDPOINT
# ---------------------------------------------------------------------------
@router.get("")
def list_messages() -> list[dict[str, Any]]:
    """Return a list of message summaries."""
    client = _client()
    try:
        # Try list_messages() or fallback to get_messages()
        if hasattr(client, "list_messages"):
            result = _require_method(client, "list_messages")()
        else:
            result = _require_method(client, "get_messages")(limit=50)

        # Explicitly cast to Iterable[Any] for type checker
        if isinstance(result, list):
            items: list[Any] = result
        elif isinstance(result, Iterable):
            items = list(result)
        else:
            # Handle unexpected single object
            items = [result]

        # Convert Email objects → JSON-safe dicts
        serialized: list[dict[str, Any]] = []
        for msg in items:
            try:
                if hasattr(msg, "model_dump"):
                    serialized.append(msg.model_dump())
                elif hasattr(msg, "dict"):
                    serialized.append(msg.dict())
                elif hasattr(msg, "__dict__"):
                    serialized.append(msg.__dict__)
                else:
                    serialized.append({"message": str(msg)})
            except Exception as e:
                serialized.append({"error": f"Serialization failed: {e}"})

        return serialized

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# GET SINGLE MESSAGE ENDPOINT
# ---------------------------------------------------------------------------
@router.get("/{message_id}")
def get_message(message_id: str) -> dict[str, Any]:
    """Return full detail for a single message."""
    client = _client()
    try:
        result = _require_method(client, "get_message")(message_id)
        if hasattr(result, "model_dump"):
            return result.model_dump()
        elif hasattr(result, "dict"):
            return result.dict()
        elif hasattr(result, "__dict__"):
            return result.__dict__
        else:
            return {"message": str(result)}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch message: {e}")


# ---------------------------------------------------------------------------
# MARK AS READ ENDPOINT
# ---------------------------------------------------------------------------
@router.post("/{message_id}/mark-as-read")
def mark_as_read(message_id: str) -> dict[str, Any]:
    """Mark a message as read."""
    client = _client()
    result = _require_method(client, "mark_as_read")(message_id)
    return cast("dict[str, Any]", result)


# ---------------------------------------------------------------------------
# DELETE MESSAGE ENDPOINT
# ---------------------------------------------------------------------------
@router.delete("/{message_id}")
def delete_message(message_id: str) -> dict[str, Any]:
    """Delete a message."""
    client = _client()
    result = _require_method(client, "delete_message")(message_id)
    return cast("dict[str, Any]", result)
