---
title: "Claude Provider Adapter"
version: "1.1.0"
type: "governance/provider"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
runtime: "claude"
---

# Claude Provider Adapter

## Purpose

Translate provider-neutral canonical governance into Claude Code syntax.

## Loading

Root `CLAUDE.md` imports the shared
[bootstrap policy](../.agents/governance/bootstrap.md) and this authored adapter.
Load the active Spec Package and current Task when repository state changes.
Read the selected canonical role and procedure before acting.
`.agents/knowledge/` and `.agents/prompts/` are canonical categories read
directly, in the order the bootstrap policy sets. Claude has no generated
projection of either, and their absence under `.claude/` is not a defect.

## Runtime Boundary

- `.claude/agents/` and `.claude/skills/` contain generated native adapters.
  Thin skill adapters point to `.agents/skills/<skill_id>/SKILL.md`; they do not
  copy procedure bodies or become a second authority.
- Generated Claude skill adapters set `disable-model-invocation: true` and are
  explicitly invoked. A discovered skill grants no additional tools or approval.
- `.claude/settings.json`, `.claude/hooks/`, and `.claude/output-styles/` are
  native mechanics that route to shared policies and scripts.
- This `provider.md` is an authored input. `.claude/README.md` and
  `.claude/CLAUDE.md` are generated pointers and never renderer inputs.
- Provider/model selections and permission translations come only from the
  [Provider Registry](../.agents/governance/providers/registry.yaml).
- Generated files may adapt syntax but do not define shared policy, role intent,
  lifecycle, templates, model selection, or completion criteria. Canonical
  `.agents/` files are never generated, quarantined, or overwritten as outputs.

## Verification

Select checks through the [shared verification matrix](../.agents/governance/quality-standards.md#5-change-type-verification-matrix)
and [completion checklist](../.agents/governance/task-checklists.md#before-completion).
The shared policy and approved Task determine scope; this adapter adds no gate.
Hook behavior remains subject to shared policy and manifest-owned public suites.
Static configuration and renderer parity prove tracked adoption only; native
invocation, hook trust, entitlement, and runtime acceptance need direct evidence.
Do not change user-global or ignored local settings under this adapter's authority.

## Related Documents

- [Canonical governance](../.agents/README.md)
- <https://code.claude.com/docs/en/sub-agents>
- <https://code.claude.com/docs/en/hooks>
