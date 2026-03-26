---
layer: agentic
title: 'Agentic Behavior Engineering Scope'
---

# Agentic Behavior Engineering Scope

Protocols for predictable, high-quality autonomous work.

## 1. Context and Objective

- Goal: standardize planning, execution, and communication.
- Priority: JIT context loading, explicit reasoning, and verifiable outputs.

## 2. Requirements and Constraints

- Keep provider-neutral rules in this scope.
- Put runtime-specific behavior in provider overlays under `providers/`.
- Use checklists from `rules/task-checklists.md` for task gating.
- Keep user-facing communication in Korean and governance text in English.

## 3. Implementation Flow

1. Start from root shim and bootstrap rules.
2. Verify permission boundaries and editable scope.
3. Execute in small, verifiable steps.
4. Validate outputs and publish evidence.

## 4. Operational Procedures

- Provide concise progress updates during long-running work.
- Stop and ask for clarification when constraints conflict.
- Prefer correcting root causes over superficial patching.

## 5. Maintenance and Safety

- Remove stale guidance and conflicting instructions immediately.
- Keep high-impact changes traceable to explicit rationale.
