"""SQLite-backed token storage for Slack OAuth."""

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TokenBundle:
    access_token: str
    scope: str
    token_type: str


class SQLiteTokenStore:
    def __init__(self, path: str = "slack_tokens.db") -> None:
        self._path = Path(path)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self._path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tokens (
                    access_token TEXT,
                    scope TEXT,
                    token_type TEXT
                )
                """
            )

    def save(self, bundle: TokenBundle) -> None:
        with sqlite3.connect(self._path) as conn:
            conn.execute("DELETE FROM tokens")
            conn.execute(
                "INSERT INTO tokens VALUES (?, ?, ?)",
                (bundle.access_token, bundle.scope, bundle.token_type),
            )

    def load(self) -> TokenBundle | None:
        with sqlite3.connect(self._path) as conn:
            cur = conn.execute("SELECT access_token, scope, token_type FROM tokens")
            row = cur.fetchone()
            if not row:
                return None
            return TokenBundle(*row)
