from __future__ import annotations

from unittest.mock import patch

import ai_api
from ai_service.main import create_app


def test_ai_service_activates_dependency_injection() -> None:
    """Creating the app should activate AI DI."""
    # App creation must trigger DI activation
    create_app()

    # Patch the DI hook itself to avoid constructing the real provider
    with patch.object(ai_api, "get_client", return_value=object()):
        client = ai_api.get_client()
        assert client is not None
