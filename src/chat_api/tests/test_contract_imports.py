def test_chat_api_imports():
    from chat_api import ChatInterface, Message, get_client
    assert ChatInterface is not None
    assert Message is not None
    assert callable(get_client)
