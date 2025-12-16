import inspect
from chat_api import ChatInterface

def test_chat_interface_methods_exist():
    methods = dict(inspect.getmembers(ChatInterface, predicate=inspect.isfunction))
    assert "send_message" in methods
    assert "get_messages" in methods
    assert "delete_message" in methods
