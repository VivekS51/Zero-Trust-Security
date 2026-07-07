"""
Decision Gateway API Models
"""

from typing import Any

from pydantic import BaseModel, Field


class DecisionRequest(BaseModel):
    policy_path: str = Field(
        ...,
        examples=["cruise/network/allow"]
    )

    input: dict[str, Any]


class DecisionResponse(BaseModel):
    allowed: bool
    policy_path: str
    decision: Any