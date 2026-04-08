# === inference.py ===
"""LLM-powered inference script for the Customer Support Routing OpenEnv.

Reads configuration from environment variables and runs all three task levels
(easy, medium, hard), logging results in strict [START]/[STEP]/[END] format.
"""

from __future__ import annotations

import json
import os
import sys
import traceback

from openai import OpenAI

from my_env.env import SupportEnv
from my_env.models import Action

# ---------------------------------------------------------------------------
# Configuration (env vars with sensible defaults)
# ---------------------------------------------------------------------------
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME: str = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN: str | None = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

MAX_STEPS = 10
ENV_NAME = "customer-support-routing"

SYSTEM_PROMPT = """\
You are an AI customer-support routing agent. For each support ticket you receive,
you must return a JSON object (no markdown, no extra text) with exactly these keys:

{
  "category": one of "billing", "technical", "general", "security", "escalation",
  "priority": one of "low", "medium", "high", "critical",
  "response": a helpful reply to the customer (at least 20 characters),
  "escalate": true or false
}

Guidelines:
- Choose the MOST RELEVANT category for the primary issue.
- Set priority based on business impact and customer tier.
- Enterprise customers with outages or SLA issues should typically be "critical".
- Set escalate=true when human intervention is clearly needed.
- Write a professional, empathetic response addressing the customer's concerns.
"""


# ---------------------------------------------------------------------------
# Logging helpers (strict format — no deviations)
# ---------------------------------------------------------------------------

def log_start(task: str, model: str) -> None:
    print(
        f"[START] task={task} env={ENV_NAME} model={model}",
        flush=True,
    )


def log_step(
    step: int,
    action_str: str,
    reward: float,
    done: bool,
    error: str | None,
) -> None:
    print(
        f"[STEP] step={step} action={action_str} "
        f"reward={reward:.2f} done={'true' if done else 'false'} "
        f"error={error if error else 'null'}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={'true' if success else 'false'} "
        f"steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# LLM interaction
# ---------------------------------------------------------------------------

def parse_action(raw: str) -> Action:
    """Parse the raw LLM response string into an Action model."""
    text = raw.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.splitlines()
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    data = json.loads(text)
    return Action(**data)


def build_user_message(obs) -> str:
    """Format an observation into the user message sent to the LLM."""
    return (
        f"Ticket ID: {obs.ticket_id}\n"
        f"Subject: {obs.subject}\n"
        f"Body: {obs.body}\n"
        f"Customer Tier: {obs.tier}\n"
        f"Sentiment: {obs.sentiment}\n"
        f"Step: {obs.step + 1}/{obs.max_steps}\n\n"
        "Respond with a JSON object only."
    )


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_task(client: OpenAI, env: SupportEnv, task_name: str) -> None:
    """Run a single task from reset to completion."""
    rewards: list[float] = []
    step_num = 0

    log_start(task_name, MODEL_NAME)

    try:
        obs = env.reset(task_name)

        for step_num in range(1, MAX_STEPS + 1):
            try:
                user_msg = build_user_message(obs)

                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_msg},
                    ],
                    temperature=0.0,
                    max_tokens=512,
                )

                raw_response = completion.choices[0].message.content or ""
                action = parse_action(raw_response)

                obs, reward, done, info = env.step(action)

                action_str = json.dumps(action.model_dump(), separators=(",", ":"))
                rewards.append(reward.score)

                log_step(step_num, action_str, reward.score, done, None)

                if done:
                    break

            except Exception as step_err:
                error_msg = str(step_err).replace("\n", " ")[:200]
                log_step(step_num, "{}", 0.0, True, error_msg)
                rewards.append(0.0)
                break

    except Exception:
        traceback.print_exc(file=sys.stderr)
        if step_num == 0:
            step_num = 1
            log_step(1, "{}", 0.0, True, "reset failed")
            rewards.append(0.0)

    score = round(sum(rewards), 2)
    success = score >= 0.6
    log_end(success, step_num, score, rewards)


def main() -> None:
    if not HF_TOKEN:
        print(
            "[WARN] No HF_TOKEN or API_KEY found in environment. "
            "LLM calls may fail.",
            file=sys.stderr,
        )

    client = OpenAI(api_key=HF_TOKEN or "dummy", base_url=API_BASE_URL)

    for task_name in ("easy", "medium", "hard"):
        run_task(client, SupportEnv(), task_name)


if __name__ == "__main__":
    main()