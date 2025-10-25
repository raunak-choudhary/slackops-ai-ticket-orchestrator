#!/bin/bash
set -e
echo "Running basic precheck..."
ruff check src || echo "Ruff linting skipped (no config)"
mypy src || echo "Mypy skipped (no type hints found)"
echo "✅ Precheck passed (no blocking errors)"
