# src/mail_client_adapter/tests/test_adapter_unit.py
from __future__ import annotations

import sys
from pathlib import Path

# Put repo root on sys.path
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from mail_client_adapter.adapter import ServiceAdapter, ServiceBackedClient  # noqa: E402


def test_adapter_exists():
    # mypy: avoid truthiness checks on callables
    assert callable(ServiceAdapter)
    assert callable(ServiceBackedClient)