from __future__ import annotations

from typing import Any


class GmailClient:
    """Minimal Gmail client used by tests.

    Notes:
        The test suite monkeypatches instance methods `fetch` and `send`.
        These stubs exist only so attribute lookup succeeds during monkeypatching.
    """

    def fetch(self) -> list[dict[str, Any]]:
        """Return a list of message dicts (stub). The test overrides this."""
        return []

    def send(self, _email: Any) -> Any:  # underscore avoids unused-arg warning
        """Send an email (stub). The test overrides this."""
        return None
