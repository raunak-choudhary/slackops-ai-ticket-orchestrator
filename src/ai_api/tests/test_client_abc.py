"""Tests for AIInterface abstract base class."""

import inspect
from abc import ABC

import pytest

from ai_api.client import AIInterface


def test_ai_interface_is_abstract() -> None:
    """AIInterface must be an abstract base class."""
    assert issubclass(AIInterface, ABC)
    assert inspect.isabstract(AIInterface)


def test_ai_interface_has_generate_response() -> None:
    """AIInterface must define generate_response method."""
    assert hasattr(AIInterface, "generate_response")
    method = AIInterface.generate_response
    assert callable(method)


def test_ai_interface_generate_response_is_abstract() -> None:
    """generate_response must be an abstract method."""
    method = AIInterface.generate_response
    assert getattr(method, "__isabstractmethod__", False)


def test_cannot_instantiate_ai_interface() -> None:
    """Instantiating AIInterface directly should fail."""
    with pytest.raises(TypeError):
        AIInterface()  # type: ignore[abstract]
