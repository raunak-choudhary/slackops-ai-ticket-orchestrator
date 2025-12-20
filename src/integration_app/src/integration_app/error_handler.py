from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UserFacingError:
    """A safe, user-facing error message for Slack."""

    message: str
    category: str
    retryable: bool = True


def _is_timeout(exc: BaseException) -> bool:
    name = exc.__class__.__name__.lower()
    return "timeout" in name


def _is_connection_error(exc: BaseException) -> bool:
    name = exc.__class__.__name__.lower()
    return "connect" in name or "connection" in name


def _http_status_code(exc: BaseException) -> int | None:
    # Optional support for httpx / requests style exceptions without importing them.
    resp = getattr(exc, "response", None)
    status = getattr(resp, "status_code", None)
    if isinstance(status, int):
        return status
    return None


def to_user_error(exc: BaseException, *, context: str) -> UserFacingError:
    """Convert an internal exception into a friendly Slack message."""
    status_code = _http_status_code(exc)

    if _is_timeout(exc):
        return UserFacingError(
            message=f"{context} timed out. Please try again.",
            category="timeout",
            retryable=True,
        )

    if _is_connection_error(exc):
        return UserFacingError(
            message=f"{context} is unavailable right now. Please try again soon.",
            category="unavailable",
            retryable=True,
        )

    if status_code is not None:
        if 500 <= status_code <= 599:
            return UserFacingError(
                message=f"{context} is temporarily unavailable (upstream error). Please try again soon.",
                category="upstream_5xx",
                retryable=True,
            )
        if status_code in (401, 403):
            return UserFacingError(
                message=f"{context} rejected the request (auth/permissions). Check credentials.",
                category="auth",
                retryable=False,
            )
        if status_code == 404:
            return UserFacingError(
                message=f"{context} endpoint was not found (404). Check configuration.",
                category="not_found",
                retryable=False,
            )

    return UserFacingError(
        message=f"{context} failed due to an unexpected error. Please try again.",
        category="unknown",
        retryable=True,
    )


def send_friendly_error(
    *,
    slack: Any,
    channel: str,
    exc: BaseException,
    context: str,
) -> None:
    """Log the exception and send a safe message to Slack."""
    user_err = to_user_error(exc, context=context)
    logger.exception(
        "%s | category=%s retryable=%s",
        context,
        user_err.category,
        user_err.retryable,
    )
    slack.send_message(channel, user_err.message)
