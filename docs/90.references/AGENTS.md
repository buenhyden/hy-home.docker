---
title: "References Agent Guide"
version: "0.2.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
---

# References Agent Guide

## Overview

Stage 90 holds non-normative evidence: research, audit and data packages that
help other stages judge facts but never decide them. This guide routes an
agent that records evidence here. The human guide is [README.md](README.md).

## Scope

`research/`, `audits/` and `data/` packages (`RES-####`, `AUD-####`,
`DATA-####`) with their members and category READMEs. A current rule, decision
or procedure never lives here.

## Working Rules

- Edit only with an authorizing request; Stage documents are read-only by
  default.
- Create a package from its pack template
  ([research](../99.templates/templates/references/research-pack.template.md),
  [audit](../99.templates/templates/references/audit-pack.template.md),
  [data](../99.templates/templates/references/data-pack.template.md)) and each
  member, `m####-<slug>.md`, from the matching member template.
- Record provenance and observation dates (`observed_at`, `reviewed_at`). A
  dated snapshot keeps its original values; record a new observation instead
  of rewriting one.
- Move a finding that should bind current behavior to its owner in Stage 01,
  02, 03 or 05; do not cite Stage 90 as authority.
- Retired package numbers go into the Registry `reserved_history`.
- Package READMEs are Korean; member documents are English.

## Canonical References

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [documentation protocol](../../.agents/governance/documentation-protocol.md),
  [stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md).
- Role: [`doc-writer`](../../.agents/roles/doc-writer.md).
- Skills: [`knowledge-map-agent`](../../.agents/skills/knowledge-map-agent/SKILL.md),
  [`workspace-audit-revalidation`](../../.agents/skills/workspace-audit-revalidation/SKILL.md).
- Knowledge routes: [repository map](../../.agents/knowledge/repository-map.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

## Verification

- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-links.py --mode language`

## Related Documents

- [References README](README.md)
- [Research pack template](../99.templates/templates/references/research-pack.template.md)
