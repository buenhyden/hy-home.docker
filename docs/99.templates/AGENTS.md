---
title: "Templates Agent Guide"
version: "0.3.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-12"
---

# Templates Agent Guide

## Scope

### Allowed Surface

Stage 99 holds the document contracts: the Registry, the schemas and the
copyable templates every other stage is validated against. This guide routes
an agent that changes them. The human guide is [README.md](README.md).

`registry.json`, `contracts/*.schema.json`, `templates/**` and this folder's
README. A change here changes what every governed document must look like.

### Non-goals

This guide does not decide policy; a rule it summarizes belongs to the canonical owner named under Required Policies.

## Required Policies

### Canonical Sources

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [documentation protocol](../../.agents/governance/documentation-protocol.md),
  [stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md),
  [quality standards](../../.agents/governance/quality-standards.md).
- Roles: [`rules-engineer`](../../.agents/roles/rules-engineer.md),
  [`qa-engineer`](../../.agents/roles/qa-engineer.md).
- Skills: [`policy-gate-agent`](../../.agents/skills/policy-gate-agent/SKILL.md),
  [`test-authoring`](../../.agents/skills/test-authoring/SKILL.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

### Local Obligations

- Templates keep `{{UPPER_SNAKE_CASE}}` placeholders and author-prompt
  comments; the authoring language follows each profile's `language`.

## Workflow

### Inspect and Change

- Treat a Registry, schema or template change as a validator change: it needs
  an authorizing Spec, a RED/GREEN test in `tests/lib/document_governance/`,
  and a corpus re-check, not a document-only review.
- Keep `registry.json` byte-stable apart from the intended change; it is
  written as two-space JSON with a trailing newline.
- Every profile needs its `transitions` and
  `archive_retention.disposition_entry_statuses` entries; a profile with a
  template also needs a `template_roles` entry. A non-docs path a profile owns
  must be listed in `scripts/lib/document_governance/registry.py`.

### Handoff

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Templates README](README.md)
- [Registry](registry.json)

## Verification

### Required Checks

- `python3 -m unittest tests.lib.document_governance.test_registry`
- `python3 scripts/validation/check-document-metadata.py --mode check-active`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- `python3 scripts/validation/check-document-links.py --mode alignment`

### Evidence and Limits

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

## Safety

### Protected Actions

- Identity spaces are append-only: never lower a `high_water` mark or drop a
  number from `reserved_history`.

### Stop and Escalate

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../../.agents/governance/approval-boundaries.md)
has not granted, or when a required check fails.
