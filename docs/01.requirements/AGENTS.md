---
title: "Requirements Agent Guide"
version: "1.0.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Requirements Agent Guide
  layer: agent
updated: "2026-11-20"
---

# Requirements Agent Guide

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the agent-guide payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Allowed Scope

###### Allowed Surface
<!-- core-payload-level:4 -->

Stage 01 holds Requirement Packages: the problem, stakeholder value, scope,
functional and quality requirements (with solution-independent interface needs
written as functional requirements),
and acceptance criteria. This guide routes an agent that changes a file here
to the owners that decide how. The human guide is [README.md](README.md).

Every `docs/01.requirements/####-<slug>.md` Requirement Package and this
folder's README.

###### Non-goals
<!-- core-payload-level:4 -->

Architecture, implementation contracts and operating procedures are out of
scope; they belong to Stage 02, Stage 03 and Stage 05.

##### Instruction Precedence

When this guide and the owner of a rule it summarizes disagree, the owner wins
and this guide is corrected
([documentation protocol](../00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd)).
[Bootstrap](../../.agents/governance/bootstrap.md#authority-and-precedence)
sets the full precedence order; a folder guide routes only and never overrides
canonical governance or a Stage contract.

#### Workflow

##### Intake

- Load order and authority: [bootstrap](../../.agents/governance/bootstrap.md).
- Authoring, identity, language and retirement rules:
  [documentation protocol](../00.workspace/03.process/documentation-protocol.md).
- Stage purposes and type families:
  [stage authoring matrix](../00.workspace/01.project/stage-authoring-matrix.md).
- Approval for Stage edits:
  [approval boundaries](../00.workspace/04.quality/approval-boundaries.md).
- Role: [`doc-writer`](../../.agents/roles/doc-writer.md). Skill:
  [`requirements-to-design-agent`](../../.agents/skills/requirements-to-design-agent/SKILL.md).
- Edit-time warnings: the
  [`warn-stage-doc-edit`](../../.agents/governance/hooks/hookify.warn-stage-doc-edit.md)
  and [`enforce-docs-templates`](../../.agents/governance/hooks/hookify.enforce-docs-templates.md)
  hook rules, delivered by `.claude/hooks/` and `.codex/hooks.json`.
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

##### Execution

###### Inspect and Change
<!-- core-payload-level:4 -->

- Create a package from the Requirement template
  [`requirement-package.template.md`](../99.templates/02.templates/01.requirements/requirement-package.template.md)
  under the Registry `requirements-package` profile: `type:
  sdlc/requirement`, `artifact_id: REQ-####`; `parent_ids` is optional and,
  when present, records only Registry-required structural relations.
- Change an existing package in place. Do not add a parallel PRD, SRS,
  interface-requirement or compatibility file.
- Add a traceability link only when the linked Description, ADR, Spec or
  Operations document exists.

###### Local Obligations
<!-- core-payload-level:4 -->

- Write child IDs in full (`REQ-####-FR-####`, `REQ-####-NFR-####`); no
  `IF` child identity is issued. Never reuse a number or lower a high-water mark; a
  retired package or child number goes into the Registry `reserved_history`.
- Keep requirements solution-independent. A requirement that names a script,
  container flag or volume path belongs to the Stage 03 Spec or Stage 05
  policy that owns the implementation.
- Write prose in English, per the profile `language`.

#### Boundaries

##### Authority

###### Stop and Escalate
<!-- core-payload-level:4 -->

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../00.workspace/04.quality/approval-boundaries.md)
has not granted, or when a required check fails.

###### Protected Actions
<!-- core-payload-level:4 -->

- Edit only with an authorizing request; Stage documents are read-only by
  default.

##### Secrets and External Effects

This guide adds no secret or external-effect rule;
[approval boundaries](../00.workspace/04.quality/approval-boundaries.md) owns both.

#### Verification

##### Checks

- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- The metadata check above loads Stage 01 and rejects a package or child
  numbering gap that `reserved_history` does not record.
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain` shows
  the selected checks without running them.

##### Reporting

###### Evidence and Limits
<!-- core-payload-level:4 -->

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

###### Handoff
<!-- core-payload-level:4 -->

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Requirement Packages README](README.md)
- [Requirement template](../99.templates/02.templates/01.requirements/requirement-package.template.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
