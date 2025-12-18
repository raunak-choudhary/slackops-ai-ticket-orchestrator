import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """
    Raised when required application configuration is missing.
    """
    pass


def _require(name: str) -> str:
    """
    Retrieve a required environment variable.

    Raises:
        ConfigError: if the variable is missing or empty.
    """
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class AppConfig:
    """
    Application configuration.

    NOTE:
    At this stage, the integration app is scoped to Slack only.
    AI and Jira configuration will be added back when those
    integrations are introduced.
    """

    # Slack
    slack_service_base_url: str


def load_config() -> AppConfig:
    """
    Load and validate application configuration.

    This function is intentionally fail-fast to ensure
    misconfiguration is detected at startup.
    """
    return AppConfig(
        slack_service_base_url=_require("SLACK_SERVICE_BASE_URL"),
    )
