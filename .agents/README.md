---
title: "AI Agent Governance"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "agent-governance"
---

# Agent Governance

## Overview

`.agents/` is the repository-owned canonical home for shared agent governance,
roles, and reusable procedures. Claude and Codex consume these sources through
native adapters. The canonical home is authored content, never renderer output.

## Scope

- `governance/` owns approval, security, quality, Git, documentation, workflow,
  bootstrap, and SDLC behavior.
- `roles/` owns stable identities, responsibilities, permissions, and handoff.
- `skills/<skill_id>/SKILL.md` owns callable procedures; skill-local
  `agents/openai.yaml` requires explicit invocation.
- `governance/providers/registry.yaml` owns provider identities, model and
  permission translations, projection routes, and hook facts.
- [Claude](../.claude/provider.md) and [Codex](../.codex/provider.md) own their
  native loading and syntax differences. Their generated READMEs are outputs.

[Stage 99](../docs/99.templates/README.md) owns document profiles, paths,
identifiers, lifecycle values, and templates. Registered scripts own executable
checks. The current Spec Package Task owns execution evidence; its preserved
Stage 98 record and Git history retain completed evidence.

## Structure

```text
.agents/
├── README.md
├── governance/
│   ├── <policy>.md
│   ├── sdlc.md
│   ├── hooks/
│   └── providers/
├── roles/
└── skills/<skill_id>/
    ├── SKILL.md
    └── agents/openai.yaml
```

Only registered canonical entries are permitted. Unknown entries are preserved
and reported for review. No common runtime, memory, installer, or generated role
surface is introduced here.

## How to Work in This Area

1. Enter through root `AGENTS.md` or `CLAUDE.md` and follow
   [bootstrap](governance/bootstrap.md).
2. Read the needed policy, role, explicitly selected skill, native adapter, and
   governing Spec Package Task. Discovery never broadens permission.
3. Change approved canonical sources and record focused evidence in the Task.
4. After an approved projection-input change, use the registered provider
   renderer's `--write` and `--check` routes. Follow the
   [exact quarantine procedure](governance/providers/README.md) when reported.
   Verify canonical source bytes were preserved and native drift is zero.
5. Select completion checks through the shared
   [quality matrix](governance/quality-standards.md#5-change-type-verification-matrix).

## Related Documents

- [SDLC](governance/sdlc.md)
- [Bootstrap](governance/bootstrap.md)
- [Provider registry](governance/providers/registry.yaml)
- [Canonical-home decision](../docs/02.architecture/decisions/0032-canonical-agent-governance-home.md)
