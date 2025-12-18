# Shared fixtures are defined locally or not required.

import pytest

pytest.skip(
    "mail_client_service tests require real service credentials",
    allow_module_level=True,
)