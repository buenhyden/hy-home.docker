---
title: "Claude Provider Adapter"
version: "1.7.2"
type: "governance/provider"
status: "active"
owner: "@buenhyden"
updated: "2026-11-12"
runtime: "claude"
---

# Claude Provider Adapter

## Overview

Translate provider-neutral canonical governance into Claude Code syntax.

## Loading

Root `CLAUDE.md` imports the shared
[bootstrap policy](../.agents/governance/bootstrap.md) and this authored adapter.
Load the active Spec Package and current Task when repository state changes.
Read the selected canonical role and procedure before acting.
Per the [Claude Code memory documentation](https://code.claude.com/docs/en/memory),
Claude Code reads `AGENTS.md` only where no `CLAUDE.md` sits on the path (its
default `claude-md-or-agents-md` mode), and the `instructionFiles` setting that
makes it read both is ignored in project settings. Root `CLAUDE.md` is on every
path here, so Claude does not read a folder `AGENTS.md` on its own. Each folder
that carries an `AGENTS.md` therefore also carries a generated `CLAUDE.md`
whose only content is the renderer marker comment, a heading and the import
`@AGENTS.md`. Claude loads a folder
`CLAUDE.md` on demand the first time it reads or writes a file below that
folder, and again on demand after compaction, so the guide reaches it
natively. The shared PreToolUse dispatcher (`scripts/hooks/agent-event-hook.sh`,
through `scripts/lib/hooks/folder_guides.py`) delivers guide content to
Claude only on an edit below a folder whose `CLAUDE.md` is missing or does not
import `@AGENTS.md`. Otherwise it adds a one-line reminder naming the nearest
folder guide on each edit, and after a SessionStart `compact` or `resume` an instruction to re-read
it. The bootstrap step that requires reading that guide applies when neither
route runs.
`.agents/knowledge/` and `.agents/prompts/` are canonical categories read
directly, in the order the bootstrap policy sets. Claude has no generated
projection of either, and their absence under `.claude/` is not a defect.

## Native Controls

- `.claude/agents/` and `.claude/skills/` contain generated native adapters.
  Thin skill adapters point to `.agents/skills/<skill_id>/SKILL.md`; they do not
  copy procedure bodies or become a second authority.
- Generated Claude skill adapters set `disable-model-invocation: true` and are
  explicitly invoked. A discovered skill grants no additional tools or approval.
- Skills are generated adapter files, not symlinks to `.agents/skills/`. A
  symlink would load the canonical `SKILL.md` as is, without
  `disable-model-invocation: true`, so Claude could start a shared skill on its
  own, and the canonical file must stay provider-neutral. Codex needs neither,
  because it reads `.agents/skills/` directly.
- `.claude/settings.json`, `.claude/hooks/`, and `.claude/output-styles/` are
  native mechanics that route to shared policies and scripts. The `.claude/hooks/`
  wrappers are authored, not rendered. The Registry PreToolUse binding's
  `on_failure: block` is written `"onFailure": "block"` here; per the Claude
  Code documentation (2.1.295 or later) a hook that then times out denies the
  tool, which has not been observed. The `permissions.deny` rules are native
  extra protection, not Registry translations: they back the
  [secret boundary](../.agents/governance/approval-boundaries.md#authorization-source-and-records)
  and the [no-direct-push rule](../.agents/governance/github-governance.md#1-repository-protection-contract).
- This `provider.md` is an authored input. `.claude/README.md` and
  `.claude/CLAUDE.md` are generated pointers and never renderer inputs. Each
  folder `CLAUDE.md` beside a folder `AGENTS.md` is a generated import shim
  that `scripts/operations/provider_surface_renderer.py` writes, checks and
  retires with its guide.
- Provider/model selections and permission translations come only from the
  [Provider Registry](../.agents/governance/providers/registry.yaml).
- Generated files may adapt syntax but do not define shared policy, role intent,
  lifecycle, templates, model selection, or completion criteria. Canonical
  `.agents/` files are never generated, quarantined, or overwritten as outputs.
- Native memory is off through `autoMemoryEnabled: false` in
  `.claude/settings.json`; no `.claude/agents/*.md` sets `memory:`.

## Limitations

Select checks through the [shared verification matrix](../.agents/governance/quality-standards.md#5-change-type-verification-matrix)
and [completion checklist](../.agents/governance/task-checklists.md#before-completion).
The shared policy and approved Task determine scope; this adapter adds no gate.
Hook behavior remains subject to shared policy and workflow-contract-owned public suites.
The [shared output contract](../.agents/governance/output-style.md) keeps
`FAIL`, `BLOCKED`, `SKIPPED`, `NOT_RUN`, partial results, and required
approval visible; this adapter cannot present any of them as completion.
Static configuration and renderer parity prove tracked configuration only; native
invocation, hook trust, entitlement, and runtime acceptance need direct evidence.
Do not change user-global or ignored local settings under this adapter's authority.

## Related Documents

- [Canonical governance](../.agents/README.md)
- <https://code.claude.com/docs/en/sub-agents>
- <https://code.claude.com/docs/en/hooks>
