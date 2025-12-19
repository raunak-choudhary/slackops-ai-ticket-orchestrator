import pytest
pytestmark = pytest.mark.integration

from integration_app.config import load_config


def test_config_loads_without_error():
    """
    Ensures required env vars are present and DI can activate.
    This should fail fast if configuration is broken.
    """
    load_config()
