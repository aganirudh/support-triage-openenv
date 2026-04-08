# === app.py ===
"""FastAPI server exposing the SupportEnv as HTTP endpoints.

Runs on port 7860 (Hugging Face Spaces default).
"""

from __future__ import annotations

import threading
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from my_env.env import SupportEnv
from my_env.models import Action, Observation

app = FastAPI(
    title="Customer Support Routing Env",
    description="OpenEnv-compliant environment for automated support ticket routing.",
    version="1.0.0",
)

# Global environment instance with a lock for thread safety.
_env = SupportEnv()
_lock = threading.Lock()


# ------------------------------------------------------------------
# Request / Response schemas
# ------------------------------------------------------------------

class ResetRequest(BaseModel):
    task_name: str = "easy"


class StepResponse(BaseModel):
    observation: dict[str, Any]
    reward: dict[str, Any]
    done: bool
    info: dict[str, Any]


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check."""
    return {"status": "ok"}


@app.post("/reset")
def reset(data: dict = None) -> dict:
    """Reset the environment to a specific task."""
    task_name = "easy"
    if data and "task_name" in data:
        task_name = data["task_name"]
    
    with _lock:
        try:
            obs = _env.reset(task_name=task_name)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return obs.model_dump()


@app.post("/step", response_model=None)
def step(action: Action) -> StepResponse:
    """Execute one step in the environment."""
    with _lock:
        try:
            obs, reward, done, info = _env.step(action)
        except RuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        return StepResponse(
            observation=obs.model_dump(),
            reward=reward.model_dump(),
            done=done,
            info=info,
        )


@app.get("/state", response_model=None)
def get_state() -> dict[str, Any]:
    """Return the current environment state."""
    with _lock:
        return _env.state()


# ------------------------------------------------------------------
# Main entry-point (for direct execution and `uv run server`)
# ------------------------------------------------------------------

def start_server() -> None:
    """Entry point for the `server` script defined in pyproject.toml.

    Called by:  uv run server
    """
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    start_server()
