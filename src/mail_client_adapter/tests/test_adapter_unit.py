# src/mail_client_adapter/tests/test_adapter_unit.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
from src.mail_client_adapter.src.mail_client_adapter.adapter import ServiceBackedClient, ServiceAdapter


def test_service_adapter_exists():
    adapter = ServiceAdapter()
    assert adapter is not None


def test_service_backed_client_exists():
    client = ServiceBackedClient()
    assert client is not None
