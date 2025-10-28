from slack_impl import SQLiteTokenStore, TokenBundle


def test_sqlite_token_store_crud_inmemory() -> None:
    store = SQLiteTokenStore()  # :memory:
    user = "U123"
    bundle = TokenBundle(access_token="xoxb-abc", scope="chat:write")

    assert store.has(user) is False
    assert store.load(user) is None

    store.save(user, bundle)
    assert store.has(user) is True
    got = store.load(user)
    assert got == bundle

    store.delete(user)
    assert store.has(user) is False
    assert store.load(user) is None