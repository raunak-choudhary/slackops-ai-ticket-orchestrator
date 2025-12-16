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
        """Test that get_client returns the injected client implementation."""
        mock_client = Mock(spec=ChatInterface)
        monkeypatch.setattr(chat_api, "get_client", lambda: mock_client)

        client = chat_api.get_client()

        assert client is mock_client

    def test_get_client_without_implementation_raises_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that get_client raises NotImplementedError."""

        def raise_not_implemented() -> ChatInterface:
            raise NotImplementedError

        monkeypatch.setattr(chat_api, "get_client", raise_not_implemented)

        with pytest.raises(NotImplementedError):
            chat_api.get_client()
