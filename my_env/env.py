# === my_env/env.py ===
"""SupportEnv — OpenEnv-compliant environment for customer-support routing."""

from __future__ import annotations

from my_env.grader import grade_with_breakdown
from my_env.models import Action, Observation, Reward
from my_env.tasks import TASKS

MAX_STEPS = 10
REPEAT_PENALTY = 0.1


class SupportEnv:
    """Multi-step environment where an agent triages support tickets."""

    def __init__(self) -> None:
        self.task_name: str = ""
        self.tickets: list[dict] = []
        self.ticket_index: int = 0
        self.step_count: int = 0
        self.cumulative_reward: float = 0.0
        self.done: bool = True
        self.current_observation: Observation | None = None
        self._last_action_json: str | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self, task_name: str = "easy") -> Observation:
        """Load a task by name and return the first observation."""
        if task_name not in TASKS:
            raise ValueError(
                f"Unknown task '{task_name}'. Choose from: {list(TASKS.keys())}"
            )

        self.task_name = task_name
        self.tickets = TASKS[task_name]
        self.ticket_index = 0
        self.step_count = 0
        self.cumulative_reward = 0.0
        self.done = False
        self._last_action_json = None

        self.current_observation = self._build_observation()
        return self.current_observation

    def step(self, action: Action) -> tuple[Observation, Reward, bool, dict]:
        """Process one agent action and advance the episode."""
        if self.done:
            raise RuntimeError("Episode is done. Call reset() first.")

        self.step_count += 1

        # --- Grade ---
        ticket = self.tickets[self.ticket_index]
        score, breakdown = grade_with_breakdown(action, ticket["expected"])

        # --- Repeat penalty ---
        action_json = action.model_dump_json()
        if action_json == self._last_action_json:
            score = max(score - REPEAT_PENALTY, 0.0)
        self._last_action_json = action_json

        self.cumulative_reward += score

        # --- Advance to next ticket or end ---
        self.ticket_index += 1
        is_terminal = (
            self.ticket_index >= len(self.tickets)
            or self.step_count >= MAX_STEPS
        )
        self.done = is_terminal

        # --- Build next observation ---
        if not self.done:
            self.current_observation = self._build_observation()
        else:
            self.current_observation = self._build_terminal_observation()

        reward = Reward(
            score=round(score, 4),
            breakdown=breakdown,
            partial=not is_terminal,
        )

        info: dict = {
            "ticket_id": ticket["ticket_id"],
            "step": self.step_count,
            "cumulative_reward": round(self.cumulative_reward, 4),
        }

        return self.current_observation, reward, self.done, info

    def state(self) -> dict:
        """Return the full current environment state."""
        return {
            "task_name": self.task_name,
            "step_count": self.step_count,
            "cumulative_reward": round(self.cumulative_reward, 4),
            "done": self.done,
            "current_observation": (
                self.current_observation.model_dump()
                if self.current_observation
                else None
            ),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_observation(self) -> Observation:
        ticket = self.tickets[self.ticket_index]
        return Observation(
            ticket_id=ticket["ticket_id"],
            subject=ticket["subject"],
            body=ticket["body"],
            tier=ticket["tier"],
            sentiment=ticket["sentiment"],
            step=self.step_count,
            max_steps=MAX_STEPS,
        )

    def _build_terminal_observation(self) -> Observation:
        """Return a sentinel observation signalling episode end."""
        return Observation(
            ticket_id="DONE",
            subject="Episode complete",
            body="All tickets have been processed.",
            tier="free",
            sentiment="neutral",
            step=self.step_count,
            max_steps=MAX_STEPS,
        )