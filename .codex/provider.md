---
title: "Codex Provider Adapter"
version: "1.1.0"
type: "governance/provider"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
runtime: "codex"
---

# Codex Provider Adapter

## Purpose

Translate provider-neutral canonical governance into Codex native syntax.

## Loading

Codex enters through root `AGENTS.md`, which explicitly instructs reading the
[bootstrap policy](../.agents/governance/bootstrap.md) and this authored adapter.
Load the active Spec Package and current Task when repository state changes.
Select a canonical role from `.agents/roles/`, read its `skill_ids`, and explicitly
read the selected `.agents/skills/<skill_id>/SKILL.md` before acting.

## Runtime Boundary

- `.codex/agents/*.toml` contains generated role adapters.
- `.agents/skills/<skill_id>/SKILL.md` is the authored native skill source.
  Its `name` and `description` support discovery; `metadata` preserves shared
  governance identity, ownership, lifecycle, and scope. Each skill's
  `agents/openai.yaml` sets `policy.allow_implicit_invocation: false`.
  Explicit canonical reads remain the loading fallback; discovery never grants
  tools, broader permissions, or implementation approval.
- `.agents/knowledge/` and `.agents/prompts/` are canonical categories read
  directly from the shared home, in the order the bootstrap policy sets. Codex
  has no generated projection of either, and their absence under `.codex/` is
  not a defect, for the same reason `.codex/skills/` is absent.
- The Provider Registry distinguishes canonical skill discovery from generated
  outputs. Codex has no generated skill projection and no `.codex/skills/` copy.
  Canonical `.agents/` is a real repository-owned source tree. Unknown entries
  are preserved and reported, never silently deleted or regenerated.
- This `provider.md` is an authored input; `.codex/README.md` is a generated
  pointer and never a renderer input. Canonical sources cannot be renderer output.
- `.codex/hooks.json` and existing repository-local configuration provide native
  mechanics only. This adapter does not require a new `.codex/config.toml`.
- Provider/model selections, reasoning controls, and sandbox translations come
  only from the [Provider Registry](../.agents/governance/providers/registry.yaml).
- Generated files adapt syntax and cannot own shared policy, role intent,
  lifecycle, templates, model selection, or completion criteria.

## Verification

Select checks through the [shared verification matrix](../.agents/governance/quality-standards.md#5-change-type-verification-matrix)
and [completion checklist](../.agents/governance/task-checklists.md#before-completion).
The shared policy and approved Task determine scope; this adapter adds no gate.
Static source structure and renderer parity do not prove live picker discovery,
skill invocation, trusted hook delivery, entitlement, or runtime acceptance.
Record those as unverified until directly observed within separate authorization.
Respect the active sandbox and approval boundary; do not mutate user-global or
ignored local configuration or install global skill copies.

## Related Documents

- [Canonical governance](../.agents/README.md)
- <https://developers.openai.com/codex/config-reference/>
