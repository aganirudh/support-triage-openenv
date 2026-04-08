---
title: Customer Support Routing Env
emoji: 🎫
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
  - reinforcement-learning
  - customer-support
---

# 🎫 Customer Support Routing Env

An **OpenEnv-compliant** environment for evaluating AI agents on automated customer support ticket routing. Agents must classify, prioritize, respond to, and optionally escalate support tickets across three difficulty tiers.

## Overview

This environment simulates a real-world customer support triage system. An AI agent receives support tickets as observations and must produce structured routing decisions (category, priority, response, escalation) that are graded against expert-defined expected answers.

## Motivation

Customer support routing is a challenging real-world task that tests:
- **Classification accuracy** — mapping free-text issues to structured categories
- **Priority judgment** — weighing business impact, customer tier, and urgency
- **Response quality** — drafting empathetic, actionable replies
- **Escalation decisions** — knowing when to involve a human agent

Frontier models often struggle with multi-issue tickets, SLA-aware prioritization, and enterprise escalation scenarios, making this a meaningful benchmark.

## Observation Space

| Field       | Type     | Description                              |
|-------------|----------|------------------------------------------|
| `ticket_id` | `str`    | Unique ticket identifier                 |
| `subject`   | `str`    | Short summary of the customer issue      |
| `body`      | `str`    | Full text of the customer message        |
| `tier`      | `str`    | `free`, `pro`, or `enterprise`           |
| `sentiment` | `str`    | `positive`, `neutral`, `negative`, `frustrated` |
| `step`      | `int`    | Current step number in the episode       |
| `max_steps` | `int`    | Maximum steps per episode (default: 10)  |

## Action Space

| Field      | Type   | Description                                         |
|------------|--------|-----------------------------------------------------|
| `category` | `str`  | `billing`, `technical`, `general`, `security`, `escalation` |
| `priority` | `str`  | `low`, `medium`, `high`, `critical`                  |
| `response` | `str`  | Drafted reply to the customer (min 1 char)           |
| `escalate` | `bool` | Whether to escalate to a human agent                 |

## Reward Function

Rewards are deterministic and range from **0.0 to 1.0**, computed as:

| Component         | Weight | Criteria               |
|--------------------|--------|------------------------|
| Category match     | 0.40   | Exact string match     |
| Priority match     | 0.30   | Exact string match     |
| Response quality   | 0.30   | Length-based thresholds |

**Response quality thresholds:**
- `<20` chars → 0.00
- `20–50` chars → 0.10
- `51–100` chars → 0.20
- `>100` chars → 0.30

A **repeat penalty** of −0.10 is applied when the agent submits an identical action consecutively.

## Tasks

### Easy
Clear single-issue tickets with obvious categories (billing, technical, general). Straightforward sentiment and low ambiguity. 3 tickets per episode.

### Medium
Ambiguous multi-issue tickets requiring judgment. Mixed sentiment, unclear primary category, feature-request overlap, and security concerns. 3 tickets per episode.

### Hard
Enterprise-grade tickets with technical jargon, SLA implications, escalation decisions, multiple nested issues, and frustrated tone. Designed to challenge frontier models on prioritization and escalation. 3 tickets per episode.

## Setup & Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run inference

```bash
export HF_TOKEN="your-huggingface-token"
python inference.py
```

### Start the API server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Validate the environment spec

```bash
python openenv.py validate
```

### Run an interactive episode

```bash
python openenv.py run --task easy
```

### Run tests

```bash
pytest test.py -v
```

## API Endpoints

| Method | Path      | Description                                    |
|--------|-----------|------------------------------------------------|
| POST   | `/reset`  | Reset env with `{"task_name": "easy"}`         |
| POST   | `/step`   | Submit an action, get observation+reward+done  |
| GET    | `/state`  | Get current environment state                  |
| GET    | `/health` | Health check → `{"status": "ok"}`              |

## Baseline Scores

| Task   | Random Agent | Qwen2.5-72B (zero-shot) |
|--------|-------------|-------------------------|
| Easy   | ~0.15       | ~0.85                   |
| Medium | ~0.10       | ~0.65                   |
| Hard   | ~0.05       | ~0.50                   |

*Scores are approximate and may vary with prompt engineering.*

## Docker Usage

```bash
docker build -t support-env .
docker run -p 7860:7860 support-env
```

The server will be available at `http://localhost:7860`.