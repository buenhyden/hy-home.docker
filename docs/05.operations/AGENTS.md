---
title: "Operations Agent Guide"
version: "1.0.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Operations Agent Guide
  layer: agent
updated: "2026-11-20"
---

# Operations Agent Guide

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

Stage 05 holds operator knowledge: Guides, Policies, Runbooks and incident
packets. This guide routes an agent that authors them or responds to an
incident. The human guide is [README.md](README.md).

`01.guides/`, `02.policies/`, `03.runbooks/` (by numbered family), `04.incidents/<year>/`
and their READMEs.

###### Non-goals
<!-- core-payload-level:4 -->

Product requirements and architecture belong to Stage 01 and Stage 02; change
execution belongs to the Stage 03 Task.

##### Instruction Precedence

When this guide and the owner of a rule it summarizes disagree, the owner wins
and this guide is corrected
([documentation protocol](../00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd)).
[Bootstrap](../../.agents/governance/bootstrap.md#authority-and-precedence)
sets the full precedence order; a folder guide routes only and never overrides
canonical governance or a Stage contract.

#### Workflow

##### Intake

- [Bootstrap](../../.agents/governance/bootstrap.md),
  [documentation protocol](../00.workspace/03.process/documentation-protocol.md),
  [approval boundaries](../00.workspace/04.quality/approval-boundaries.md),
  [environment constraints](../../.agents/governance/environment-constraints.md).
- Roles: [`doc-writer`](../../.agents/roles/doc-writer.md),
  [`incident-responder`](../../.agents/roles/incident-responder.md).
- Skills: [`ops-runbook-agent`](../../.agents/skills/ops-runbook-agent/SKILL.md),
  [`incident-response`](../../.agents/skills/incident-response/SKILL.md),
  [`stateful-recovery-contract-review`](../../.agents/skills/stateful-recovery-contract-review/SKILL.md).
- Hook rules: [`warn-stage-doc-edit`](../../.agents/governance/hooks/hookify.warn-stage-doc-edit.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

##### Execution

###### Inspect and Change
<!-- core-payload-level:4 -->

- Author from the operations templates:
  [guide](../99.templates/02.templates/05.operations/guide.template.md),
  [policy](../99.templates/02.templates/05.operations/policy.template.md),
  [runbook](../99.templates/02.templates/05.operations/runbook.template.md),
  [incident](../99.templates/02.templates/05.operations/incident.template.md),
  [postmortem](../99.templates/02.templates/05.operations/postmortem.template.md).
  Identities are `GDE-####`, `POL-####`, `RUN-####` and `inc-YYYY-####`.
- Store incident packets only at
  `04.incidents/<year>/inc-####-<slug>/incident.md` and `postmortem.md`.

###### Local Obligations
<!-- core-payload-level:4 -->

- A Guide's `implementation_services` must name the exact Compose path and
  service it documents; the operations catalog joins Guides, Policies and
  Runbooks to Compose, so do not add a parallel service registry.
- Stage 05 operations documents are Korean; this agent guide is English.

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

- Never write a secret value; name a secret only by its file or reference.
- A procedure step that changes live runtime, remote settings or stateful data
  is executed only under its own approval; documenting it grants none.

#### Verification

##### Checks

- `python3 scripts/validation/check-operations-catalog.py`
- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`

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

- [Operations README](README.md)
- [Runbook template](../99.templates/02.templates/05.operations/runbook.template.md)

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
