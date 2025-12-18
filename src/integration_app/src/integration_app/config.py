import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    pass


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class AppConfig:
    # Slack
    slack_service_base_url: str

    # AI
    ai_service_base_url: str
    openai_api_key: str

    # Jira
    jira_base_url: str
    jira_email: str
    jira_api_token: str
    jira_project_key: str


def load_config() -> AppConfig:
    return AppConfig(
        slack_service_base_url=_require("SLACK_SERVICE_BASE_URL"),
        ai_service_base_url=_require("AI_SERVICE_BASE_URL"),
        openai_api_key=_require("OPENAI_API_KEY"),
        jira_base_url=_require("JIRA_BASE_URL"),
        jira_email=_require("JIRA_EMAIL"),
        jira_api_token=_require("JIRA_API_TOKEN"),
        jira_project_key=_require("JIRA_PROJECT_KEY"),
    )
