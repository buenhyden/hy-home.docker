---
title: Agent Bootstrap Policy
type: governance/policy
layer: agent-governance
status: active
owner: "@buenhyden"
---

# Agent Bootstrap Policy

## Purpose

Provide the sole repository bootstrap sequence for supported agents.

## Canonical Load Order

1. Enter through root `AGENTS.md` or `CLAUDE.md`.
2. Load this policy, the matching adapter in `providers/`, and only the
   provider facts required from `providers/registry.yaml`.
3. Resolve only the Stage 00 policies, canonical role, and skills needed for
   the request.
4. For repository changes, load the governing Requirements, Architecture, and
   Spec Package plus its current Task.
5. Execute the applicable registered gates and record evidence in that Task.

Root shims and adapters route to this sequence and do not define alternatives.

## Authority and Precedence

1. Direct system and user instructions.
2. Stage 00 policies, including workflow and approval behavior.
3. Canonical Stage 00 roles and skills, which implement but cannot override
   policy.
4. Current stage documents under Stage 99 path, profile, identifier, and
   lifecycle contracts.
5. Provider Registry translation facts, provider adapters, and native runtime
   mechanics.
6. Stage 90 evidence and non-authoritative historical material.

The Provider Registry owns provider identities, projection routes, model and
permission translations, and hook/event bindings only. Stage 99 owns document
paths and profiles. Neither namespace may redefine Stage 00 policy. Generated
and tracked native runtime controls are consumers, never policy sources.
Execution progress and handoff state belong to the current Task; Git history is
the recovery mechanism.

## Hard Constraints

- Stage 00 remains English-only.
- Stage documents are read-only unless the request authorizes change.
- Keep root shims concise.
- Never write plaintext credentials or secret values.
- Treat the Graphify report as advisory whenever its commit differs from HEAD.
- Use in-place canonical edits; do not create legacy redirects or parallel
  authority copies.

## Verification Routing

Use [task-checklists.md](task-checklists.md) for completion and
[approval-boundaries.md](approval-boundaries.md) for protected surfaces. Stage
99 owns document shapes; registered scripts own executable checks.
