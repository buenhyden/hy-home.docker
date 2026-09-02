---
title: Codex Provider Adapter
version: 1.0.0
type: governance/provider
status: active
owner: "@buenhyden"
runtime: codex
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
- `.agents/skills/*/SKILL.md` is the generated shared skill projection used by
  Codex; `.codex/skills/` is not a separate source.
- `.codex/hooks.json` and repository-local Codex configuration provide runtime
  mechanics only.
- Provider/model selections, reasoning controls, and sandbox translations come
  only from `registry.yaml`.
- Generated files may adapt syntax but may not define policy, roles, lifecycle,
  templates, model selection, or completion criteria.

## Verification

Run `python3 scripts/validation/run-ci-gate.py --profile full`. Respect the
active sandbox and approval boundary; do not mutate user-global configuration
without explicit authorization.

## Related Documents

- <https://developers.openai.com/codex/config-reference/>
