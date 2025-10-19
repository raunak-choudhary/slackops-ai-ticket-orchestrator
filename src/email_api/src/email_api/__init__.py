"""
Stable nested email_api package initializer.
Prevents circular imports and resolves top-level Client import safely.
"""

import importlib.util
import sys
from pathlib import Path

# Compute path to src/email_api/client.py
root_path = Path(__file__).resolve().parents[2] / "client.py"
if root_path.exists():
    spec = importlib.util.spec_from_file_location("email_api.client", root_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["email_api.client"] = mod
    spec.loader.exec_module(mod)

# Expose Client only if it exists
try:
    from email_api.client import Client  # type: ignore
except Exception:
    Client = None  # fallback
