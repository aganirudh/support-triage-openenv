# === my_env/grader.py ===
"""Deterministic grader for customer-support routing actions.

Scoring breakdown (total 1.0):
    category match   — 0.40  (exact string match)
    priority match   — 0.20  (exact string match)
    escalate match   — 0.10  (boolean match)
    response content — 0.30  (length-based + keyword-based)
"""

from __future__ import annotations

from my_env.models import Action


def _response_score(response: str, hint: str = "") -> float:
    """Score response based on length and keyword hints.
    
    Max score: 0.30
    - Length credit: up to 0.20
    - Keyword credit: up to 0.10
    """
    score = 0.0
    length = len(response)
    
    # Length credit
    if length > 100:
        score += 0.20
    elif length > 50:
        score += 0.15
    elif length >= 20:
        score += 0.10
        
    # Keyword credit (check for common hint words)
    keywords = [w.lower() for w in hint.replace(",", "").replace(".", "").split() if len(w) > 3]
    if keywords:
        matches = sum(1 for k in keywords if k in response.lower())
        match_ratio = matches / len(keywords)
        score += min(match_ratio * 0.10, 0.10)
    else:
        # Fallback if no hint keywords: give automatic content credit if response is long
        if length > 150:
            score += 0.10
            
    return round(score, 2)


def grade_with_breakdown(action: Action, expected: dict) -> tuple[float, dict]:
    """Return both the total score and a per-component breakdown."""
    cat = 0.40 if action.category == expected["category"] else 0.0
    pri = 0.20 if action.priority == expected["priority"] else 0.0
    esc = 0.10 if action.escalate == expected.get("escalate", False) else 0.0
    
    resp = _response_score(action.response, expected.get("response_hint", ""))

    breakdown = {
        "category_score": cat,
        "priority_score": pri,
        "escalate_score": esc,
        "response_score": resp,
    }
    
    # Final score is the sum of all components
    total_score = cat + pri + esc + resp
    
    # PHASE 2 COMPLIANCE: Ensure score is strictly between 0 and 1 (0.01 - 0.99)
    # This prevents absolute 0.0 or 1.0 as required by the validator.
    total_score = max(0.01, min(0.99, total_score))
    
    return total_score, breakdown


def grade(action: Action, expected: dict) -> float:
    score, _ = grade_with_breakdown(action, expected)
    return score