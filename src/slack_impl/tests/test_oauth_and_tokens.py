"""Tests for OAuth helpers and token storage."""

from slack_impl.oauth import build_authorization_url
from slack_impl.token_store import SQLiteTokenStore, TokenBundle


def test_build_authorization_url_contains_required_params() -> None:
    """Authorization URL includes client_id, scopes, and redirect_uri."""
    url = build_authorization_url(
        client_id="abc",
        redirect_uri="http://localhost",
        scopes=["chat:write", "channels:read"],
    )

    assert "client_id=abc" in url
    assert "redirect_uri=http%3A%2F%2Flocalhost" in url
    assert "chat%3Awrite" in url


def test_token_store_save_and_load(tmp_path) -> None:
    """TokenBundle can be saved and reloaded."""
    db_path = tmp_path / "tokens.db"
    store = SQLiteTokenStore(str(db_path))

    bundle = TokenBundle(
        access_token="xoxb",
        scope="chat:write",
        token_type="bot",
    )

    store.save(bundle)
    loaded = store.load()

    assert loaded is not None
    assert loaded.access_token == "xoxb"
    assert loaded.scope == "chat:write"
