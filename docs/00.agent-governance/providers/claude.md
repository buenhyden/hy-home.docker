---
profile_id: governance-provider
layer: agentic
runtime: claude
status: active
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

Run `python3 scripts/validation/run-ci-gate.py --profile full`. Hook behavior
remains subject to the shared policy and manifest-owned public suites.

## Related Documents

- <https://code.claude.com/docs/en/sub-agents>
- <https://code.claude.com/docs/en/hooks>
