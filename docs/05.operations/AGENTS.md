---
title: "Operations Agent Guide"
version: "0.2.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
---

# Operations Agent Guide

## Overview

Stage 05 holds operator knowledge: Guides, Policies, Runbooks and incident
packets. This guide routes an agent that authors them or responds to an
incident. The human guide is [README.md](README.md).

## Scope

`guides/`, `policies/`, `runbooks/` (by numbered family), `incidents/<year>/`
and their READMEs. Product requirements and architecture belong to Stage 01
and Stage 02; change execution belongs to the Stage 03 Task.

## Working Rules

- Edit only with an authorizing request; Stage documents are read-only by
  default.
- Author from the operations templates:
  [guide](../99.templates/templates/operations/guide.template.md),
  [policy](../99.templates/templates/operations/policy.template.md),
  [runbook](../99.templates/templates/operations/runbook.template.md),
  [incident](../99.templates/templates/operations/incident.template.md),
  [postmortem](../99.templates/templates/operations/postmortem.template.md).
  Identities are `GDE-####`, `POL-####`, `RUN-####` and `inc-YYYY-####`.
- A Guide's `implementation_services` must name the exact Compose path and
  service it documents; the operations catalog joins Guides, Policies and
  Runbooks to Compose, so do not add a parallel service registry.
- Store incident packets only at
  `incidents/<year>/inc-####-<slug>/incident.md` and `postmortem.md`.
- Never write a secret value; name a secret only by its file or reference.
- A procedure step that changes live runtime, remote settings or stateful data
  is executed only under its own approval; documenting it grants none.
- Stage 05 operations documents are Korean; this agent guide is English.

## Canonical References

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [documentation protocol](../../.agents/governance/documentation-protocol.md),
  [approval boundaries](../../.agents/governance/approval-boundaries.md),
  [environment constraints](../../.agents/governance/environment-constraints.md).
- Roles: [`doc-writer`](../../.agents/roles/doc-writer.md),
  [`incident-responder`](../../.agents/roles/incident-responder.md).
- Skills: [`ops-runbook-agent`](../../.agents/skills/ops-runbook-agent/SKILL.md),
  [`incident-response`](../../.agents/skills/incident-response/SKILL.md),
  [`stateful-recovery-contract-review`](../../.agents/skills/stateful-recovery-contract-review/SKILL.md).
- Hook rules: [`warn-stage-doc-edit`](../../.agents/governance/hooks/hookify.warn-stage-doc-edit.md),
  [`warn-docker-infra-stop`](../../.agents/governance/hooks/hookify.warn-docker-infra-stop.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

## Verification

- `python3 scripts/validation/check-operations-catalog.py`
- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`

## Related Documents

- [Operations README](README.md)
- [Runbook template](../99.templates/templates/operations/runbook.template.md)
