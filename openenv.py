# === openenv.py ===
"""CLI wrapper for the Customer Support Routing OpenEnv.

Usage:
    python openenv.py validate            — check openenv.yaml exists and is valid
    python openenv.py run --task easy      — run one interactive episode
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from my_env.env import SupportEnv
from my_env.models import Action


# ------------------------------------------------------------------
# validate sub-command
# ------------------------------------------------------------------

REQUIRED_KEYS = {"name", "version", "description", "entrypoint", "tasks", "reward"}


def cmd_validate(args: argparse.Namespace) -> None:
    """Check that openenv.yaml exists and contains required fields."""
    yaml_path = Path(__file__).parent / "openenv.yaml"
    if not yaml_path.exists():
        print(f"[ERROR] {yaml_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)

    if not isinstance(spec, dict):
        print("[ERROR] openenv.yaml root must be a mapping.", file=sys.stderr)
        sys.exit(1)

    missing = REQUIRED_KEYS - spec.keys()
    if missing:
        print(f"[ERROR] Missing required keys: {missing}", file=sys.stderr)
        sys.exit(1)

    tasks = spec.get("tasks", [])
    if not isinstance(tasks, list) or len(tasks) == 0:
        print("[ERROR] 'tasks' must be a non-empty list.", file=sys.stderr)
        sys.exit(1)

    print("[OK] openenv.yaml is valid.")
    print(f"     Name   : {spec['name']}")
    print(f"     Version: {spec['version']}")
    print(f"     Tasks  : {[t.get('name', t) if isinstance(t, dict) else t for t in tasks]}")


# ------------------------------------------------------------------
# run sub-command
# ------------------------------------------------------------------

def cmd_run(args: argparse.Namespace) -> None:
    """Run one episode interactively via stdin prompts."""
    task_name: str = args.task
    env = SupportEnv()
    obs = env.reset(task_name)

    print(f"\n=== Episode: {task_name} ===\n")

    while not env.done:
        print(f"--- Step {env.step_count + 1} ---")
        print(f"Ticket : {obs.ticket_id}")
        print(f"Subject: {obs.subject}")
        print(f"Body   : {obs.body}")
        print(f"Tier   : {obs.tier}   Sentiment: {obs.sentiment}")
        print()

        category = input("Category [billing/technical/general/security/escalation]: ").strip() or "general"
        priority = input("Priority [low/medium/high/critical]: ").strip() or "medium"
        response = input("Response: ").strip() or "Thank you for contacting us."
        escalate_str = input("Escalate? [y/N]: ").strip().lower()
        escalate = escalate_str in ("y", "yes", "true", "1")

        action = Action(
            category=category,
            priority=priority,
            response=response,
            escalate=escalate,
        )

        obs, reward, done, info = env.step(action)

        print(f"\n  Reward : {reward.score:.2f}  Breakdown: {json.dumps(reward.breakdown)}")
        print(f"  Done   : {done}   Cumulative: {info.get('cumulative_reward', 0):.2f}")
        print()

    state = env.state()
    print("=== Episode Complete ===")
    print(f"Total steps : {state['step_count']}")
    print(f"Total reward: {state['cumulative_reward']:.2f}")


# ------------------------------------------------------------------
# Argument parser
# ------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openenv",
        description="CLI for the Customer Support Routing OpenEnv.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("validate", help="Validate openenv.yaml")

    run_parser = sub.add_parser("run", help="Run an interactive episode")
    run_parser.add_argument(
        "--task",
        type=str,
        default="easy",
        choices=["easy", "medium", "hard"],
        help="Task difficulty level (default: easy)",
    )

    args = parser.parse_args()

    if args.command == "validate":
        cmd_validate(args)
    elif args.command == "run":
        cmd_run(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
