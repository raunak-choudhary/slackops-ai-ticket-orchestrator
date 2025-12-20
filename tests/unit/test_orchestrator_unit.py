import pytest
from chat_api.client import Message


class ConcreteMessage(Message):
    """
    Concrete test-only Message implementation to
    execute abstract property bodies.
    """

    @property
    def id(self) -> str:
        return super().id

    @property
    def content(self) -> str:
        return super().content

    @property
    def sender_id(self) -> str:
        return super().sender_id


def test_message_interface_properties_raise_not_implemented():
    msg = ConcreteMessage()

    with pytest.raises(NotImplementedError):
        _ = msg.id

    with pytest.raises(NotImplementedError):
        _ = msg.content

    with pytest.raises(NotImplementedError):
        _ = msg.sender_id
