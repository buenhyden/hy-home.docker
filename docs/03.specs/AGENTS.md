---
title: "Specifications Agent Guide"
version: "1.0.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Specifications Agent Guide
  layer: agent
updated: "2026-11-20"
---

# Specifications Agent Guide

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

Stage 03 holds Spec Packages: a Spec contracts the change, a Plan sequences
it, and Tasks record execution and evidence. This guide routes an agent that
creates or executes a package. The human guide is [README.md](README.md).

`####-<slug>/spec.md`, `plan.md`, `01.tasks/tsk-####-<slug>.md`, `02.contracts/` and
this folder's README.

###### Non-goals
<!-- core-payload-level:4 -->

Long-lived requirements, architecture and operating procedures belong to Stage
01, Stage 02 and Stage 05.

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
  [SDLC](../00.workspace/03.process/sdlc.md),
  [workflows](../../.agents/governance/workflows.md),
  [documentation protocol](../00.workspace/03.process/documentation-protocol.md),
  [task checklists](../00.workspace/04.quality/task-checklists.md),
  [quality standards](../00.workspace/04.quality/quality-standards.md).
- Roles: [`workflow-supervisor`](../../.agents/roles/workflow-supervisor.md),
  [`code-reviewer`](../../.agents/roles/code-reviewer.md).
- Skills: [`execution-plan-agent`](../../.agents/skills/execution-plan-agent/SKILL.md),
  [`task-breakdown-agent`](../../.agents/skills/task-breakdown-agent/SKILL.md),
  [`change-review-execution`](../../.agents/skills/change-review-execution/SKILL.md).
- Prompt: [handoff](../../.agents/prompts/handoff.md).
- Provider loading: [Claude adapter](../../.claude/provider.md),
  [Codex adapter](../../.codex/provider.md).

##### Execution

###### Inspect and Change
<!-- core-payload-level:4 -->

- Load the governing Spec, Plan and current Task before any repository change,
  and record progress, decisions and evidence in that Task.
- Create documents from
  [`spec.template.md`](../99.templates/02.templates/03.specs/spec.template.md),
  [`plan.template.md`](../99.templates/02.templates/03.specs/plan.template.md) and
  [`task.template.md`](../99.templates/02.templates/03.specs/task.template.md).
  Allocate the next Spec number from the Registry `spec` space and advance its
  high-water mark in the same change.
- Record each check as an Evidence row with an honest result from the
  Registry `result_domain` in [`registry.json`](../99.templates/registry.json)
  and the revision it examined. What a row may
  `Resolve` is defined by the [SDLC](../00.workspace/03.process/sdlc.md#sequence)
  and the Registry `evidence_columns` contract.
- Remove a package only as the
  [retirement preconditions](../00.workspace/03.process/documentation-protocol.md#retirement-preconditions)
  and the [SDLC](../00.workspace/03.process/sdlc.md#sequence) readiness and
  approval sequence define it.

###### Local Obligations
<!-- core-payload-level:4 -->

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

- Never edit the body of a terminal Task. Record a later correction in the
  current Task instead.

##### Secrets and External Effects

This guide adds no secret or external-effect rule;
[approval boundaries](../00.workspace/04.quality/approval-boundaries.md) owns both.

#### Verification

##### Checks

- `python3 scripts/validation/check-document-corpus-lifecycle.py`
- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`
- `python3 scripts/validation/check-document-links.py --mode alignment`
- `python3 scripts/validation/check-document-links.py --mode commands`

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

- [Specifications README](README.md)
- [Task template](../99.templates/02.templates/03.specs/task.template.md)

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
