"""
Global pytest configuration for slack_adapter tests.

Makes the generated client (clients/python/slack_chat_service_hw2_client)
importable so adapter.py can `from slack_chat_service_hw2_client.client import Client`.
"""

import os
import sys

# tests/ -> slack_adapter/ -> src/ -> <repo root>
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CLIENTS_PATH = os.path.join(REPO_ROOT, "clients", "python")

if CLIENTS_PATH not in sys.path:
    sys.path.insert(0, CLIENTS_PATH)
