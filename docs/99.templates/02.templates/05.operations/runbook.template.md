---
title: '{{TITLE}}'
version: 0.1.0
type: operation/runbook
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
layer: operations
artifact_id: '{{ARTIFACT_ID}}'
created: '{{CREATED}}'
next_review_at: '{{NEXT_REVIEW_AT}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the runbook payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: Name the maintained subject, scope and owner; do not grant authority through document metadata. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: State actual inputs, constraints or preconditions, and distinguish facts from assumptions. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: Keep the kind-specific payload here with its conditions, tables and one canonical responsibility. -->

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

#### Trigger and Scope

##### Trigger

{{WHEN_TO_USE_AND_EXPECTED_OUTCOME}}

##### Targets

<!-- Author prompt: Name the exact targets, environments and services this runbook covers, what it leaves out, and link the implementation and policy that own them. -->

{{TARGETS_BOUNDARIES_AND_AUTHORITY_LINKS}}

#### Preflight

##### Authority

<!-- Author prompt: Name the approval this runbook needs, who may run it, and the access and secret names (never values) required. -->

{{APPROVAL_OPERATOR_ACCESS_AND_SECRET_NAMES}}

##### Environment

{{BACKUP_STARTING_STATE_AND_READ_ONLY_PREFLIGHT}}

#### Procedure

##### Steps

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. State exact targets, preconditions, approval and safety boundaries, static checks, symptom-led diagnosis and logs, authorized start, stop, and restart actions, backup and restore, upgrade and migration, ordered commands, expected results, stop conditions, verification, rollback or recovery, escalation, and evidence handoff. Use only commands proven executable in the current image or host implementation. For a non-service workspace subject, keep only actions its implementation actually supports. Separate read-only checks from runtime mutations; never print secrets or full rendered private configuration. Preserve data during rollback; backup restoration requires an isolated rehearsal before claiming recovery. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

<!-- Author prompt: The table lists each step in order: Step is its number, Action the permitted action, Expected Result what to observe, and On Failure where to stop and who takes over. Commands and detail follow the table. -->

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| {{STEP}} | {{ACTION}} | {{EXPECTED_RESULT}} | {{ON_FAILURE}} |

{{ORDERED_ACTIONS_AND_EXPECTED_RESULTS}}

##### Stop Conditions

{{CONDITIONS_THAT_STOP_THE_PROCEDURE}}

#### Verification

##### Expected Results

<!-- Author prompt: Say what evidence to record and where; never record secrets or full rendered private configuration. -->

{{SERVICE_CHECKS_AND_EVIDENCE_TO_RECORD}}

##### Unverified Conditions

<!-- Author prompt: Name what this runbook has not been observed to do, such as a step never run against the current implementation, and state the observation that would verify it. -->

{{CONDITIONS_NOT_YET_OBSERVED}}

#### Escalation

##### Next Owner

{{ESCALATION_OWNER_AND_HANDOFF}}

##### Recovery or Forward Repair

<!-- Author prompt: Preserve data during rollback, and require an isolated rehearsal before claiming backup recovery. When the procedure changes no state, say that no rollback applies and name the forward repair. -->

{{ROLLBACK_RECOVERY_OR_FORWARD_REPAIR}}

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: Explain how the intended reader uses this document or its native output; do not invent an operational step. -->

Use the procedures or reading order stated in the role payload.

### 확인 기준

<!-- 작성 규칙: Use only checks appropriate to this kind; distinguish implementation, verification and actual acceptance. -->

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: Use purpose-bearing owner and dependency references; reciprocal links are not universally required. -->

The role payload retains the current owner and dependency references.

### 외부 근거

<!-- 작성 규칙: Identify external basis and its application or limits; a citation grants no execution or approval authority. -->

External basis and its limits remain those stated in the role payload; a citation grants no authority.
