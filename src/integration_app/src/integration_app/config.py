"""
Centralized configuration loader for the integration application.

Validates required environment variables at startup so that
misconfiguration fails fast and clearly.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


def load_config() -> None:
    """Load and validate required environment variables."""
    required_vars = [
        "SLACK_SERVICE_BASE_URL",
        "AI_SERVICE_BASE_URL",
        "JIRA_SERVICE_BASE_URL",
        "OPENAI_API_KEY",
    ]

    for var in required_vars:
        if not os.environ.get(var):
            logger.critical("Missing required environment variable: %s", var)
            raise ConfigError(f"Missing required environment variable: {var}")

    logger.info("Integration app configuration loaded successfully")
