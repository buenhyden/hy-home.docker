---
profile_id: governance-policy
layer: agentic
status: active
---

# Agent Bootstrap Policy

## Purpose

Provide the sole repository bootstrap sequence for supported agents.

## Canonical Load Order

1. Enter through root `AGENTS.md` or `CLAUDE.md`.
2. Load this policy and the matching adapter in `providers/`.
3. Resolve only the policies, role, and skills needed for the request.
4. For repository changes, load the governing Requirements, Architecture, and
   Spec Package plus its current Task.
5. Execute the applicable registered gates and record evidence in that Task.

Root shims and adapters route to this sequence and do not define alternatives.

## Authority and Precedence

1. Direct system and user instructions.
2. Stage 00 policies and roles.
3. Stage 99 document authority.
4. Current stage documents according to their registered roles.
5. Provider adapters and runtime mechanics.
6. Stage 90 evidence and Stage 98 history.

Generated projections are never policy sources. Execution progress and handoff
state belong to the current Task; Git history is the recovery mechanism.

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
