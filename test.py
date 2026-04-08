# === test.py ===
"""Pytest test suite for the Customer Support Routing OpenEnv."""

from __future__ import annotations

import pytest

from my_env.env import SupportEnv
from my_env.grader import grade, grade_with_breakdown
from my_env.models import Action, Observation, Reward


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def env() -> SupportEnv:
    return SupportEnv()


def _perfect_easy_action() -> Action:
    """An action that matches easy ticket #1 expectations perfectly."""
    return Action(
        category="billing",
        priority="medium",
        response=(
            "I sincerely apologize for the billing discrepancy on your invoice. "
            "I have escalated this to our billing team and they will correct the "
            "amount from $149 back to the quoted $99 within 24 hours."
        ),
        escalate=False,
    )


def _zero_score_action() -> Action:
    """An action that scores 0 on every component."""
    return Action(
        category="security",
        priority="critical",
        response="ok",
        escalate=True,
    )


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------

class TestReset:
    def test_reset_returns_observation(self, env: SupportEnv) -> None:
        obs = env.reset("easy")
        assert isinstance(obs, Observation)
        assert obs.ticket_id == "EASY-001"
        assert obs.step == 0
        assert obs.max_steps == 10

    def test_reset_with_invalid_task_raises(self, env: SupportEnv) -> None:
        with pytest.raises(ValueError, match="Unknown task"):
            env.reset("nonexistent")


class TestStep:
    def test_step_returns_valid_reward(self, env: SupportEnv) -> None:
        env.reset("easy")
        action = _perfect_easy_action()
        obs, reward, done, info = env.step(action)
        assert isinstance(reward, Reward)
        assert isinstance(reward.score, float)
        assert isinstance(reward.breakdown, dict)
        assert "category_score" in reward.breakdown

    def test_reward_in_range(self, env: SupportEnv) -> None:
        env.reset("easy")
        action = _perfect_easy_action()
        _, reward, _, _ = env.step(action)
        assert 0.0 <= reward.score <= 1.0


class TestState:
    def test_state_returns_dict(self, env: SupportEnv) -> None:
        env.reset("easy")
        state = env.state()
        assert isinstance(state, dict)
        assert "task_name" in state
        assert "step_count" in state
        assert "cumulative_reward" in state
        assert "done" in state
        assert "current_observation" in state
        assert state["task_name"] == "easy"


class TestGrader:
    def test_grader_perfect_score(self) -> None:
        action = _perfect_easy_action()
        expected = {"category": "billing", "priority": "medium"}
        score = grade(action, expected)
        assert score == 1.0

    def test_grader_zero_score(self) -> None:
        action = _zero_score_action()
        expected = {"category": "billing", "priority": "medium"}
        score = grade(action, expected)
        assert score == 0.0

    def test_grader_partial_score(self) -> None:
        action = Action(
            category="billing",
            priority="high",
            response="Short reply here.",
            escalate=False,
        )
        expected = {"category": "billing", "priority": "medium"}
        score = grade(action, expected)
        # category match (0.4) + priority miss (0.0) + response <20 chars (0.0)
        assert score == pytest.approx(0.4)


class TestEpisode:
    def test_episode_terminates(self, env: SupportEnv) -> None:
        env.reset("easy")
        done = False
        steps = 0
        while not done and steps < 15:
            action = _perfect_easy_action()
            _, _, done, _ = env.step(action)
            steps += 1
        assert done is True
        assert steps <= 10

    def test_determinism(self, env: SupportEnv) -> None:
        """Same action on the same task must produce the same score."""
        action = _perfect_easy_action()

        env.reset("easy")
        _, r1, _, _ = env.step(action)

        env.reset("easy")
        _, r2, _, _ = env.step(action)

        assert r1.score == r2.score
        assert r1.breakdown == r2.breakdown