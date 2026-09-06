---
title: "Agent Bootstrap Policy"
version: "1.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
---

# Agent Bootstrap Policy

## Purpose

Provide the sole repository bootstrap sequence for supported agents.

## Canonical Load Order

1. Enter through root `AGENTS.md` or `CLAUDE.md`.
2. Load this policy, the matching authored `.claude/provider.md` or
   `.codex/provider.md` adapter, and only the provider facts required from
   `.agents/governance/providers/registry.yaml`.
3. Resolve only the agent governance policies, canonical role, and skills needed for
   the request. Read `.agents/knowledge/` when the request needs to find which
   surface owns something, and `.agents/prompts/` when it produces a handoff, a
   diff review, a commit message, or a test design. Neither grants a tool, a
   path, a permission, or an approval; the selected role's permission profile
   still governs, and the canonical owner a knowledge member routes to remains
   the authority for what it says.
4. For repository changes, load the governing Requirements, Architecture, and
   Spec Package plus its current Task.
5. Execute the applicable registered gates and record evidence in that Task.

Root shims and adapters route to this sequence and do not define alternatives.

## Authority and Precedence

1. Direct system and user instructions.
2. Canonical governance policies, including workflow and approval behavior.
3. Canonical roles and explicitly invoked skills, which implement but cannot
   override policy.
4. Current stage documents under Stage 99 path, profile, identifier, and
   lifecycle contracts.
5. Provider Registry translation facts, provider adapters, and native runtime
   mechanics.
6. Stage 90 evidence and non-authoritative historical material.

The Provider Registry owns provider identities, projection routes, model and
permission translations, and hook/event bindings only. Stage 99 owns document
paths and profiles. Neither namespace may redefine agent governance policy. Generated
native role/skill projections and tracked runtime controls are consumers, never
shared policy sources. Authored native provider documents own syntax and loading
differences only. Canonical `.agents/` content is never a generated output.
Execution progress and handoff state belong to the current Task. A document that
leaves an active stage is preserved under `docs/98.archive/`; Git history proves
that preserved record is what was removed.

## Hard Constraints

- Canonical governance, roles, skills, knowledge, prompts, and native provider
  sources remain English-only.
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
