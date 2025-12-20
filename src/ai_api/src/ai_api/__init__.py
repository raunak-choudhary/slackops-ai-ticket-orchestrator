"""AI API Component.

This component provides abstract interfaces for AI client functionality,
following clean architecture principles with dependency injection support.

The interfaces define the contract for AI operations without implementation details,
allowing for multiple AI provider implementations (OpenAI, Anthropic, etc.).

This component focuses on the core requirement: generating responses from AI systems
based on user input and system prompts.

Example usage:
    from ai_api import AIInterface, get_client

    client = get_client()
    result = client.generate_response(
        user_input="Hello",
        system_prompt="Be friendly"
    )
"""

from ai_api.client import (
    AIInterface as AIInterface,
)
from ai_api.client import (
    get_client as get_client,
)

__version__ = "0.1.0"
__description__ = "AI client interface component"
