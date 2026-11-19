---
title: "Templates Agent Guide"
version: "0.4.2"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-19"
---

# Templates Agent Guide

## Scope

### Allowed Scope

#### Allowed Surface

Stage 99 holds the document contracts: the Registry, the schemas and the
copyable templates every other stage is validated against. This guide routes
an agent that changes them. The human guide is [README.md](README.md).

`registry.json`, `contracts/*.schema.json`, `templates/**` and this folder's
README. A change here changes what every governed document must look like.

#### Non-goals

This guide does not decide policy; a rule it summarizes belongs to the canonical owner named under Intake.

### Instruction Precedence

When this guide and the owner of a rule it summarizes disagree, the owner wins
and this guide is corrected
([documentation protocol](../00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd)).
[Bootstrap](../../.agents/governance/bootstrap.md#authority-and-precedence)
sets the full precedence order; a folder guide routes only and never overrides
canonical governance or a Stage contract.

## Workflow

### Intake

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [documentation protocol](../00.workspace/03.process/documentation-protocol.md),
  [stage authoring matrix](../00.workspace/01.project/stage-authoring-matrix.md),
  [quality standards](../00.workspace/04.quality/quality-standards.md).
- Roles: [`rules-engineer`](../../.agents/roles/rules-engineer.md),
  [`qa-engineer`](../../.agents/roles/qa-engineer.md).
- Skills: [`policy-gate-agent`](../../.agents/skills/policy-gate-agent/SKILL.md),
  [`test-authoring`](../../.agents/skills/test-authoring/SKILL.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

### Execution

#### Inspect and Change

- Treat a Registry, schema or template change as a validator change: it needs
  an authorizing Spec, a RED/GREEN test in `tests/lib/document_governance/`,
  and a corpus re-check, not a document-only review.
- Keep `registry.json` byte-stable apart from the intended change; it is
  written as two-space JSON with a trailing newline.
- Every profile needs its `transitions` and
  `archive_retention.disposition_entry_statuses` entries; a profile with a
  template also needs a `template_roles` entry. A non-docs path a profile owns
  must be listed in `scripts/lib/document_governance/registry.py`.

#### Local Obligations

- Templates keep `{{UPPER_SNAKE_CASE}}` placeholders and author-prompt
  comments; the authoring language follows each profile's `language`.

## Boundaries

### Authority

#### Stop and Escalate

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../00.workspace/04.quality/approval-boundaries.md)
has not granted, or when a required check fails.

#### Protected Actions

- Identity spaces are append-only: never lower a `high_water` mark or drop a
  number from `reserved_history`.

### Secrets and External Effects

This guide adds no secret or external-effect rule;
[approval boundaries](../00.workspace/04.quality/approval-boundaries.md) owns both.

## Verification

### Checks

- `python3 -m unittest tests.lib.document_governance.test_registry`
- `python3 scripts/validation/check-document-metadata.py --mode check-active`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- `python3 scripts/validation/check-document-links.py --mode alignment`

### Reporting

#### Evidence and Limits

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

#### Handoff

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Templates README](README.md)
- [Registry](registry.json)
