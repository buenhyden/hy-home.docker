---
layer: agentic
title: "Agentic Behavior Engineering Rule"
---

# Agentic Behavior Engineering Rule

This rule standardizes agent behavior for planning, execution, and reporting.

## 1. Context & Objective

- Keep outcomes deterministic, verifiable, and context-efficient.
- Prioritize explicit assumptions and traceable decisions over implicit behavior.

## 2. Requirements & Constraints

- Start with non-mutating discovery before any change.
- For multi-step work, produce an implementation plan before edits.
- Use persona routing and scope routing before task execution.
- Keep user-facing communication in Korean; keep governance docs in English.

## 3. Implementation Flow

1. Bootstrap: load `rules/bootstrap.md`.
2. Persona: load `rules/persona.md` and announce active persona/layer.
3. Scope: load one primary `scopes/<layer>.md`.
4. Execute smallest correct change.
5. Verify programmatic checks and summarize evidence.

## 4. Operational Procedures

- Provide concise progress updates during long-running operations.
- Stop and request clarification when constraints conflict.
- Prefer root-cause analysis over patching symptoms.

## 5. Maintenance & Safety

- Keep policy text short and actionable.
- Remove contradictory guidance immediately.
- Prefer additive governance evolution with explicit change rationale.
