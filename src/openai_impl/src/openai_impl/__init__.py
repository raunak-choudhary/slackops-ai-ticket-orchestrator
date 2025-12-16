"""OpenAI implementation for the AI API.

Importing this module activates dependency injection by registering
the OpenAI-backed AI client with the ai_api package.
"""

from ai_api import client as ai_client_api

from openai_impl.openai_client import OpenAIClient


def _get_openai_client() -> OpenAIClient:
    """Create and return an OpenAI-backed AI client."""
    return OpenAIClient()


# Monkey-patch the AI API dependency injection hook
ai_client_api.get_client = _get_openai_client
