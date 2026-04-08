# === my_env/grader.py ===
"""Deterministic grader for customer-support routing actions.

Scoring breakdown (total 1.0):
    category match   — 0.40  (exact string match)
    priority match   — 0.30  (exact string match)
    response quality — 0.30  (length-based thresholds)
"""

from __future__ import annotations

from my_env.models import Action


def _response_score(response: str) -> float:
    """Score response quality purely by character length.

    Thresholds:
        < 20 chars  → 0.00
        20–50 chars → 0.10
        51–100 chars → 0.20
        > 100 chars → 0.30
    """
    length = len(response)
    if length > 100:
        return 0.30
    if length > 50:
        return 0.20
    if length >= 20:
        return 0.10
    return 0.00


def grade(action: Action, expected: dict) -> float:
    """Grade an action against the expected answer.

    Parameters
    ----------
    action : Action
        The agent's routing decision.
    expected : dict
        Must contain ``category`` (str) and ``priority`` (str) keys.

    Returns
    -------
    float
        A score between 0.0 and 1.0.
    """
    score = 0.0

    # Category match — 0.40
    if action.category == expected["category"]:
        score += 0.40

    # Priority match — 0.30
    if action.priority == expected["priority"]:
        score += 0.30

    # Response quality — up to 0.30
    score += _response_score(action.response)

    return min(score, 1.0)


def grade_with_breakdown(action: Action, expected: dict) -> tuple[float, dict]:
    """Return both the total score and a per-component breakdown."""
    cat = 0.40 if action.category == expected["category"] else 0.0
    pri = 0.30 if action.priority == expected["priority"] else 0.0
    resp = _response_score(action.response)

    total = min(cat + pri + resp, 1.0)
    breakdown = {
        "category_score": cat,
        "priority_score": pri,
        "response_score": resp,
    }
    return total, breakdown