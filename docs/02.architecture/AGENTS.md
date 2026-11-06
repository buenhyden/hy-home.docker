---
title: "Architecture Agent Guide"
version: "0.2.2"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
---

# Architecture Agent Guide

## Overview

Stage 02 holds Architecture Descriptions, the current structure, and
Architecture Decision Records, the durable decisions. This guide routes an
agent that changes a file here. The human guide is [README.md](README.md).

## Scope

`descriptions/####-<slug>.md` (`AD-####`), `decisions/####-<slug>.md`
(`ADR-####`) and the READMEs of this folder. Requirements, change contracts and
operating procedures belong to Stage 01, Stage 03 and Stage 05.

## Working Rules

- Edit only with an authorizing request; Stage documents are read-only by
  default.
- Create a Description from
  [`description.template.md`](../99.templates/templates/architecture/description.template.md)
  and an ADR from
  [`decision.template.md`](../99.templates/templates/architecture/decision.template.md),
  under the `architecture-description` and `adr` profiles.
- A new ADR enters as `proposed`, the initial status of the
  `architecture-decision` lifecycle in the [Registry](../99.templates/registry.json);
  the [SDLC](../../.agents/governance/sdlc.md) owns the ADR states.
- Replace an accepted ADR only through a separately approved new ADR; do not
  rewrite an accepted decision body. Per
  [ADR-0051](decisions/0051-summarize-and-delete-retirement.md) and the
  [documentation protocol](../../.agents/governance/documentation-protocol.md),
  the new ADR summarizes the replaced decision in its Traceability, the old
  ADR is deleted in the same change, and its number goes into the Registry
  `reserved_history`. Stage 02 uses no `supersedes` or `superseded_by`
  metadata and no `deprecated` or `superseded` status.
- ADR-0002's `AI Agent Guidance` subsection is part of that accepted decision
  record, kept as written; current agent working rules come from this guide
  and canonical governance, not from that subsection.
- Keep the root to `README.md`, `AGENTS.md`, `descriptions/` and `decisions/`;
  the Stage 02 loader rejects any other root entry.
- Change a Description or ADR in place; do not add a replacement or redirect
  file. When summarizing a decision, keep its alternatives, rationale,
  consequences and supersession.
- Do not record a secret value, an unobserved runtime state or an interface
  that does not exist as an architecture fact.
- Retired numbers go into the Registry `reserved_history`; do not link a
  retired identity.
- Write prose in English, per the profile `language`.

## Canonical References

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [documentation protocol](../../.agents/governance/documentation-protocol.md),
  [stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md),
  [approval boundaries](../../.agents/governance/approval-boundaries.md).
- Roles: [`doc-writer`](../../.agents/roles/doc-writer.md),
  [`rules-engineer`](../../.agents/roles/rules-engineer.md) for governance
  review.
- Skills: [`adr-writing`](../../.agents/skills/adr-writing/SKILL.md),
  [`requirements-to-design-agent`](../../.agents/skills/requirements-to-design-agent/SKILL.md).
- Hook rules: [`warn-stage-doc-edit`](../../.agents/governance/hooks/hookify.warn-stage-doc-edit.md),
  [`enforce-docs-templates`](../../.agents/governance/hooks/hookify.enforce-docs-templates.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

## Verification

- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`

## Related Documents

- [Architecture README](README.md)
- [Description template](../99.templates/templates/architecture/description.template.md)
- [Decision template](../99.templates/templates/architecture/decision.template.md)
