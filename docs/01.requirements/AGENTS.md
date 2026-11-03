---
title: "Requirements Agent Guide"
version: "0.1.0"
type: "governance/agent-guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-03"
---

# Requirements Agent Guide

## Overview

Stage 01 holds Requirement Packages: the problem, stakeholder value, scope,
functional, non-functional and solution-independent interface requirements,
and acceptance criteria. This guide routes an agent that changes a file here
to the owners that decide how. The human guide is [README.md](README.md).

## Scope

Every `docs/01.requirements/####-<slug>.md` Requirement Package and this
folder's README. Architecture, implementation contracts and operating
procedures are out of scope; they belong to Stage 02, Stage 03 and Stage 05.

## Working Rules

- Edit only with an authorizing request; Stage documents are read-only by
  default.
- Create a package from the Requirement template
  [`requirement-package.template.md`](../99.templates/templates/requirements/requirement-package.template.md)
  under the Registry `requirements-package` profile: `type:
  sdlc/requirement`, `artifact_id: REQ-####`; `parent_ids` is optional and,
  when present, records only Registry-required structural relations.
- Change an existing package in place. Do not add a parallel PRD, SRS,
  interface-requirement or compatibility file.
- Write child IDs in full (`REQ-####-FR-####`, `REQ-####-NFR-####`,
  `REQ-####-IF-####`). Never reuse a number or lower a high-water mark; a
  retired package or child number goes into the Registry `reserved_history`.
- Keep requirements solution-independent. A requirement that names a script,
  container flag or volume path belongs to the Stage 03 Spec or Stage 05
  policy that owns the implementation.
- Add a traceability link only when the linked Description, ADR, Spec or
  Operations document exists.
- Write prose in English, per the profile `language`.

## Canonical References

- Load order and authority: [bootstrap](../../.agents/governance/bootstrap.md).
- Authoring, identity, language and retirement rules:
  [documentation protocol](../../.agents/governance/documentation-protocol.md).
- Stage purposes and type families:
  [stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md).
- Approval for Stage edits:
  [approval boundaries](../../.agents/governance/approval-boundaries.md).
- Role: [`doc-writer`](../../.agents/roles/doc-writer.md). Skill:
  [`requirements-to-design-agent`](../../.agents/skills/requirements-to-design-agent/SKILL.md).
- Edit-time warnings: the
  [`warn-stage-doc-edit`](../../.agents/governance/hooks/hookify.warn-stage-doc-edit.md)
  and [`enforce-docs-templates`](../../.agents/governance/hooks/hookify.enforce-docs-templates.md)
  hook rules, delivered by `.claude/hooks/` and `.codex/hooks.json`.
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

## Verification

- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- The metadata check above loads Stage 01 and rejects a package or child
  numbering gap that `reserved_history` does not record.
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain` shows
  the selected checks without running them.

## Related Documents

- [Requirement Packages README](README.md)
- [Requirement template](../99.templates/templates/requirements/requirement-package.template.md)
