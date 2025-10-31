from gmail_impl.gmail_client import GmailClient


def test_fetch_and_send_stubs_are_callable() -> None:
    c = GmailClient()
    # Call the stubs directly (in addition to the existing monkeypatch tests)
    assert isinstance(c.fetch(), list)
    assert c.send(None) is None