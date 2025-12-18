import pytest
from unittest.mock import Mock

import chat_api
from chat_api import ChatInterface


@pytest.mark.unit
class TestClientInjection:
    """Test client dependency injection pattern."""

    def test_get_client_returns_injected_implementation(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """
        Test that get_client returns the injected client implementation.

        This test validates the happy-path DI behavior:
        once an implementation is injected, get_client must
        return that concrete instance.
        """
        mock_client = Mock(spec=ChatInterface)

        # Inject implementation by replacing get_client
        monkeypatch.setattr(chat_api, "get_client", lambda: mock_client)

        client = chat_api.get_client()

        assert client is mock_client

    def test_get_client_without_implementation_raises_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """
        Test that get_client raises NotImplementedError when
        no implementation has been injected.

        This validates the explicit DI contract failure behavior
        defined by the Chat API interface.
        """

        def raise_not_implemented() -> ChatInterface:
            raise NotImplementedError

        # Simulate absence of injected implementation
        monkeypatch.setattr(chat_api, "get_client", raise_not_implemented)

        with pytest.raises(NotImplementedError):
            chat_api.get_client()
