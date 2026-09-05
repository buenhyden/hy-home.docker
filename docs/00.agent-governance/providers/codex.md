---
title: "Codex Provider Adapter"
version: "1.0.1"
type: "governance/provider"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
runtime: "codex"
---

# Codex Provider Adapter

## Purpose

Translate provider-neutral Stage 00 sources into Codex runtime syntax.

## Loading

Codex enters through root `AGENTS.md`, then loads the canonical
[bootstrap policy](../policies/bootstrap.md) and this adapter. Load the active
Spec Package and current Task when repository state changes.

## Runtime Boundary

- `.codex/agents/*.toml` is a generated role adapter surface.
- Reusable procedures are read directly from
  `docs/00.agent-governance/skills/<skill_id>.md`. Select the role in `roles/`,
  read its `skill_ids`, and explicitly load those canonical files before acting.
  Generated Codex role instructions contain the same repository-relative paths.
- The registry declares `native_skill_pattern: null` for Codex. No shared skill
  projection or `.codex/skills/` substitute is generated. This intentionally does
  not provide native `$skill` picker discovery; explicit canonical loading is
  the supported repository route. Do not recreate the retired `.agents/` tree,
  install global copies, or claim runtime acceptance from static configuration.
- `.codex/hooks.json` and repository-local Codex configuration provide runtime
  mechanics only.
- Provider/model selections, reasoning controls, and sandbox translations come
  only from `registry.yaml`.
- Generated files may adapt syntax but may not define policy, roles, lifecycle,
  templates, model selection, or completion criteria.

## Verification

Select checks through the [shared change-type verification matrix](../policies/quality-standards.md#5-change-type-verification-matrix)
and [completion checklist](../policies/task-checklists.md#before-completion).
This adapter does not add a separate gate or require the full profile for every
change. The shared policy and the approved Task determine the verification scope.

Respect the active sandbox and approval boundary; do not mutate user-global
configuration without explicit authorization.

## Related Documents

- <https://developers.openai.com/codex/config-reference/>
