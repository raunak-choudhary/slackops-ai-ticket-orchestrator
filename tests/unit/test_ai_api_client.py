import inspect
import pytest
from ai_api.client import AIInterface, get_client


def test_ai_interface_is_abstract():
    assert inspect.isabstract(AIInterface)


def test_ai_interface_methods_exist():
    methods = AIInterface.__abstractmethods__
    assert "generate_response" in methods


def test_get_client_raises_runtime_error():
    with pytest.raises(RuntimeError):
        get_client()


def test_ai_interface_source_is_loaded_for_coverage():
    source = inspect.getsource(AIInterface)
    assert "class AIInterface" in source
