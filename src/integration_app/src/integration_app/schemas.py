from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel


class JiraAction(BaseModel):
    action: Literal[
        "list_tickets",
        "create_ticket",
        "no_op",
    ]

    title: Optional[str] = None
    description: Optional[str] = None
