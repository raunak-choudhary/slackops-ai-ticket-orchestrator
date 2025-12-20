import pytest

from ai_api import client as ai_client
from chat_api import client as chat_client


def test_ai_api_get_client_raises_runtime_error():
    """
    AI API explicitly documents that get_client()
    raises RuntimeError when no implementation is registered.
    """
    with pytest.raises(RuntimeError):
        ai_client.get_client()


def test_chat_api_get_client_raises_not_implemented():
    """
    Chat API explicitly documents that get_client()
    raises NotImplementedError when no implementation is injected.
    """
    with pytest.raises(NotImplementedError):
        chat_client.get_client()
