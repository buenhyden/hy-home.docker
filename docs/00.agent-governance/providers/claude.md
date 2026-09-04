---
title: "Claude Provider Adapter"
version: "1.0.1"
type: "governance/provider"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
runtime: "claude"
---

# Claude Provider Adapter

## Purpose

Translate provider-neutral Stage 00 sources into Claude Code syntax.

## Loading

The root `CLAUDE.md` imports the canonical
[bootstrap policy](../policies/bootstrap.md) and this adapter. Load the active
Spec Package and current Task when repository state changes.

## Runtime Boundary

- `.claude/agents/` and `.claude/skills/` are generated projections.
- `.claude/settings.json`, `.claude/hooks/`, and `.claude/output-styles/` are
  Claude-native mechanics that must route to shared policies and scripts.
- Provider/model selections and permission translations come only from
  `registry.yaml`.
- Generated files may adapt syntax but may not define policy, roles, lifecycle,
  templates, model selection, or completion criteria.

## Verification

Select checks through the [shared change-type verification matrix](../policies/quality-standards.md#5-change-type-verification-matrix)
and [completion checklist](../policies/task-checklists.md#before-completion).
This adapter does not add a separate gate or require the full profile for every
change. The shared policy and the approved Task determine the verification scope.

Hook behavior remains subject to shared policy and manifest-owned public suites.

## Related Documents

- <https://code.claude.com/docs/en/sub-agents>
- <https://code.claude.com/docs/en/hooks>
