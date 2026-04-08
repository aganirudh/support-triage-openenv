# === my_env/models.py ===
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Observation(BaseModel):
    """A single support ticket presented to the agent."""

    ticket_id: str
    subject: str
    body: str
    tier: Literal["free", "pro", "enterprise"]
    sentiment: Literal["positive", "neutral", "negative", "frustrated"]
    step: int = 0
    max_steps: int = 10


class Action(BaseModel):
    """The agent's routing decision for a ticket."""

    category: Literal["billing", "technical", "general", "security", "escalation"]
    priority: Literal["low", "medium", "high", "critical"]
    response: str = Field(..., min_length=1)
    escalate: bool = False


class Reward(BaseModel):
    """Grading result for a single step."""

    score: float = Field(..., ge=0.0, le=1.0)
    breakdown: dict = Field(
        default_factory=lambda: {
            "category_score": 0.0,
            "priority_score": 0.0,
            "response_score": 0.0,
        }
    )
    partial: bool = True