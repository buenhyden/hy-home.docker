---
layer: agentic
title: "Agentic Behavior Engineering Rule"
---

# Agentic Behavior Engineering Rule

Standard behavior contract for planning, execution, and reporting.

## 1. Context and Objective

- Keep outcomes deterministic, verifiable, and context-efficient.
- Prefer explicit assumptions and traceable decisions over implicit behavior.

## 2. Requirements and Constraints

- Start with non-mutating discovery before any change.
- Produce implementation plans for multi-step work before edits.
- Use persona routing and scope routing before task execution.
- Keep governance text in English and user-facing responses in Korean by default.

## 3. Implementation Flow

1. Bootstrap via `rules/bootstrap.md`.
2. Load persona via `rules/persona.md` and announce active persona/layer.
3. Load `rules/task-checklists.md` and run pre-task gate.
4. Load one primary scope from `scopes/<layer>.md`.
5. Execute smallest correct change.
6. Run completion checklist and summarize verification evidence.

## 4. Operational Procedures

- Provide concise progress updates during long operations.
- Stop and request clarification when constraints conflict.
- Prefer root-cause analysis over symptom patching.

## 5. Maintenance and Safety

- Keep policy text short and actionable.
- Remove contradictory guidance immediately.
- Keep provider-specific behavior in provider files, not in generic scope/rule files.
