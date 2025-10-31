import pytest

from email_api.client import Client, Email


def test_send_and_list_and_get_and_delete_happy_path() -> None:
    c = Client()
    e = Email(sender="a@x", recipient="b@y", subject="s", body="b")
    ok = c.send_email(e)
    assert ok is True

    all_msgs = c.list_emails()
    assert len(all_msgs) == 1
    assert all_msgs[0].subject == "s"

    first = c.get_email(0)
    assert first is not None
    assert first.sender == "a@x"

    # delete returns True when index is valid
    assert c.delete_email(0) is True
    assert c.list_emails() == []


def test_get_and_delete_out_of_range_falsey() -> None:
    c = Client()
    # nothing sent -> out of bounds
    assert c.get_email(0) is None
    assert c.delete_email(0) is False


def test_send_email_requires_sender_and_recipient() -> None:
    c = Client()
    # relaxed regex to match message regardless of capitalization
    with pytest.raises(ValueError, match=r"[Ss]ender"):
        c.send_email(Email(sender="", recipient="b@y"))
    with pytest.raises(ValueError, match=r"[Rr]ecipient"):
        c.send_email(Email(sender="a@x", recipient=""))
