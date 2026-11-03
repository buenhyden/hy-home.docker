---
title: "Templates Agent Guide"
version: "0.1.0"
type: "governance/agent-guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-03"
---

# Templates Agent Guide

## Overview

Stage 99 holds the document contracts: the Registry, the schemas and the
copyable templates every other stage is validated against. This guide routes
an agent that changes them. The human guide is [README.md](README.md).

## Scope

`registry.json`, `contracts/*.schema.json`, `templates/**` and this folder's
README. A change here changes what every governed document must look like.

## Working Rules

- Treat a Registry, schema or template change as a validator change: it needs
  an authorizing Spec, a RED/GREEN test in `tests/lib/document_governance/`,
  and a corpus re-check, not a document-only review.
- Keep `registry.json` byte-stable apart from the intended change; it is
  written as two-space JSON with a trailing newline.
- Every profile needs its `template_roles`, `transitions` and
  `archive_retention.disposition_entry_statuses` entries, and every non-docs
  path it owns must be listed in `scripts/lib/document_governance/registry.py`.
- Identity spaces are append-only: never lower a `high_water` mark or drop a
  number from `reserved_history`.
- Templates keep `{{UPPER_SNAKE_CASE}}` placeholders and author-prompt
  comments; the authoring language follows each profile's `language`.

## Canonical References

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

## Verification

- `python3 -m unittest tests.lib.document_governance.test_registry`
- `python3 scripts/validation/check-document-metadata.py --mode check-active`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- `python3 scripts/validation/check-document-links.py --mode alignment`

## Related Documents

- [Templates README](README.md)
- [Registry](registry.json)
