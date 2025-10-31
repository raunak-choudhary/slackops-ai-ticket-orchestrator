from .adapter import (
    Channel,
    Message,
    ServiceAdapter,
    ServiceBackedClient,
    SlackServiceBackedClient,  # alias
)

__all__ = [
    "ServiceBackedClient",
    "SlackServiceBackedClient",
    "ServiceAdapter",
    "Channel",
    "Message",
]
