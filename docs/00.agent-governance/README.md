---
title: "AI Agent Governance"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "agent-governance"
---

# AI Agent Governance

## Overview

Stage 00 is the sole human and AI-agent authority for policy, roles, delegation,
handoff, provider differences, and reusable procedures. Claude and Codex are the
only supported providers. Runtime directories are generated adapters and never
own policy.

## Scope

- `policies/` owns normative approval, security, quality, Git, documentation,
  workflow, and SDLC constraints.
- `roles/` owns responsibilities, permissions, inputs, outputs, and handoff.
- `skills/` owns reusable provider-neutral procedures.
- `providers/` owns only Claude/Codex capability and syntax differences.
- `sdlc.md` owns the Requirements to Operations lifecycle.

Document profiles, paths, identifiers, lifecycle states, and template mappings
belong to [Stage 99](../99.templates/README.md). Executable enforcement belongs
to registered scripts. Current execution state belongs to the active Spec
Package Task. After disposition, the preserved Stage 98 Task is durable
evidence; Git history proves that record and does not replace its body.

## Structure

```text
00.agent-governance/
├── README.md
├── sdlc.md
├── policies/
├── roles/
├── providers/
└── skills/
```

No other active top-level entry is permitted.

## How to Work in This Area

1. Enter through `AGENTS.md` or `CLAUDE.md`.
2. Follow [bootstrap policy](policies/bootstrap.md).
3. Load only the policy, role, skill, provider adapter, and stage documents
   needed for the active request.
4. Record implementation and verification evidence in the active Task.
5. Regenerate adapters with
   `python3 scripts/operations/provider_surface_renderer.py --write`;
   treat any provider quarantine as a nonzero exact-path cleanup handoff under
   [Provider adapters](providers/README.md), then prove `--check` drift 0.

## Related Documents

- [SDLC](sdlc.md)
- [Bootstrap policy](policies/bootstrap.md)
- [Provider registry](providers/registry.yaml)
- [Stage 99 authority](../99.templates/README.md)
- [Governance authority decision](../02.architecture/decisions/0029-workspace-governance-authority.md)
