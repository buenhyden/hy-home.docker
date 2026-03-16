---
title: 'ADR 0010: Lazy-Loading Agent Rules'
status: 'Proposed'
date: '2026-03-14'
owner: 'Antigravity'
layer: 'architecture'
---

# ADR-0024: Lazy-Loading Agent Rules

## Context

As the repository grows, the "Agents Instruction" (`AGENTS.md`) and the gateway have become congested. Agents load too much context that is irrelevant to their specific task, causing higher token costs and potential confusion (hallucinations).

## Decision

We will implement an "Intent-Based Lazy Loading" protocol.

1. `AGENTS.md` remains the thin entrypoint.
2. `docs/agentic/gateway.md` serves as the map.
3. Every major task type (Refactoring, Deploying, Debugging) will have a dedicated "Rule" file in `docs/agentic/rules/`.
4. Agents must load only the rule corresponding to their current task intent.

## Consequences

- **Positive**: Reduced context overhead, higher precision in task execution, easier maintenance of task-specific rules.
- **Negative**: Adds 1-2 steps to the agent's startup sequence.
