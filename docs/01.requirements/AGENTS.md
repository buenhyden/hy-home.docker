---
title: "Requirements Agent Guide"
version: "0.3.1"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-12"
---

# Requirements Agent Guide

## Scope

### Allowed Surface

Stage 01 holds Requirement Packages: the problem, stakeholder value, scope,
functional and quality requirements (with solution-independent interface needs
written as functional requirements),
and acceptance criteria. This guide routes an agent that changes a file here
to the owners that decide how. The human guide is [README.md](README.md).

Every `docs/01.requirements/####-<slug>.md` Requirement Package and this
folder's README.

### Non-goals

Architecture, implementation contracts and operating procedures are out of
scope; they belong to Stage 02, Stage 03 and Stage 05.

## Required Policies

### Canonical Sources

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

### Local Obligations

- Write child IDs in full (`REQ-####-FR-####`, `REQ-####-NFR-####`); no
  `IF` child identity is issued. Never reuse a number or lower a high-water mark; a
  retired package or child number goes into the Registry `reserved_history`.
- Keep requirements solution-independent. A requirement that names a script,
  container flag or volume path belongs to the Stage 03 Spec or Stage 05
  policy that owns the implementation.
- Write prose in English, per the profile `language`.

## Workflow

### Inspect and Change

- Create a package from the Requirement template
  [`requirement-package.template.md`](../99.templates/templates/requirements/requirement-package.template.md)
  under the Registry `requirements-package` profile: `type:
  sdlc/requirement`, `artifact_id: REQ-####`; `parent_ids` is optional and,
  when present, records only Registry-required structural relations.
- Change an existing package in place. Do not add a parallel PRD, SRS,
  interface-requirement or compatibility file.
- Add a traceability link only when the linked Description, ADR, Spec or
  Operations document exists.

### Handoff

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Requirement Packages README](README.md)
- [Requirement template](../99.templates/templates/requirements/requirement-package.template.md)

## Verification

### Required Checks

- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- The metadata check above loads Stage 01 and rejects a package or child
  numbering gap that `reserved_history` does not record.
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain` shows
  the selected checks without running them.

### Evidence and Limits

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

## Safety

### Protected Actions

- Edit only with an authorizing request; Stage documents are read-only by
  default.

### Stop and Escalate

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../../.agents/governance/approval-boundaries.md)
has not granted, or when a required check fails.
