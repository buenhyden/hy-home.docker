---
title: '{{TITLE}}'
version: 0.1.0
type: sdlc/plan
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
layer: specs
artifact_id: '{{ARTIFACT_ID}}'
parent_ids:
- '{{PARENT_ID}}'
created: '{{CREATED}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the plan payload below for this document's information and judgments.

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
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Map each stable W-number to one or more numbered acceptance criteria without creating a second lifecycle or approval record. -->
<!-- Author prompt: A Plan holds strategy only. Execution state and check results live in the Task; link to it instead of copying them. -->

#### Overview

##### Outcome

<!-- Author prompt: Name the parent Spec and what this Plan delivers. -->

{{PARENT_SPEC_AND_OUTCOME}}

##### Constraints

<!-- Author prompt: Separate facts from assumptions, and name the constraints and the authority this Plan works under. -->

{{ASSUMPTIONS_CONSTRAINTS_AND_AUTHORITY}}

#### Dependencies

##### Prerequisites

{{EXISTING_CONTRACTS_CONSUMERS_PERMISSIONS_AND_ENVIRONMENT}}

##### Shared Resources

<!-- Author prompt: Name the files, services and environments more than one work unit or Task touches, and how their use is ordered. -->

{{SHARED_RESOURCES_AND_THEIR_ORDER}}

#### Work Breakdown

##### Work Units

<!-- Author prompt: Keep the Work Units header, separator, and every data row in one contiguous pipe-table block, and put no other pipe table under Work Breakdown. Work Unit is a stable W-number; Outcome what it delivers; Depends On `None` or earlier W-numbers; Owner the same-package Task or Tasks that execute it; Write Scope the paths it may change; Acceptance the numbered Spec criteria it serves; Checks the Check IDs it selects. -->

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| {{WORK_UNIT}} | {{OUTCOME}} | {{DEPENDS_ON}} | {{OWNER_TASK}} | {{WRITE_SCOPE}} | {{ACCEPTANCE}} | {{CHECKS}} |

##### Dependency Edges

<!-- Author prompt: State each work unit's inputs and outputs, the order the Depends On column implies, the change method and the rollback order. -->

{{WORK_UNIT_ORDER_CHANGE_AND_ROLLBACK}}

#### Verification Plan

##### Selected Checks

<!-- Author prompt: List each check the work units select: Check ID is a stable identifier in this Plan, Guarantee what only that check proves, Input what it reads, Trust Boundary what it does not prove, Required When the condition that selects it, and Evidence the kind of observation it must produce. -->

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| {{CHECK_ID}} | {{GUARANTEE}} | {{INPUT}} | {{TRUST_BOUNDARY}} | {{REQUIRED_WHEN}} | {{EVIDENCE}} |

##### Evidence Plan

<!-- Author prompt: Say which checks run at commit, push, pull request and merge without running the same check twice, who produces the evidence, and what stops the work. -->

{{CHECK_STAGES_EVIDENCE_PRODUCERS_AND_STOP_CONDITIONS}}

#### Promotion Map

##### Durable Owners

<!-- Author prompt: Name the contract or operating meaning that outlives this package and the current document that will hold it. -->

{{DURABLE_MEANING_AND_OWNER_DOCUMENTS}}

##### Consumer Updates

<!-- Author prompt: For each durable meaning, name the intended change, the consumers to update, the handoff condition and the Task whose Promotion Receipt will record it. Do not copy the receipt or any Task result here. -->

{{CONSUMER_UPDATES_AND_TASK_RECEIPT}}

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
