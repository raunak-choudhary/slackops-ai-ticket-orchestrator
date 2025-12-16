from chat_api import ChatInterface, Message
from abc import ABC

def test_chat_interface_is_abc():
    assert issubclass(ChatInterface, ABC)

def test_message_is_abc():
    assert issubclass(Message, ABC)
