---
title: '{{TITLE}}'
version: 0.1.0
type: operation/incident
status: open
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
document_lifecycle: draft
updated: '{{UPDATED}}'
layer: operations
artifact_id: '{{ARTIFACT_ID}}'
parent_ids:
- '{{PARENT_ID}}'
created: '{{CREATED}}'
occurred_at: '{{OCCURRED_AT}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the incident payload below for this document's information and judgments.

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
<!-- Author prompt: When status becomes `resolved`, add `resolved_at` (ISO 8601 with UTC offset) after `occurred_at`; the status requires it. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

#### Impact

##### Affected Users

{{AFFECTED_USERS}}

##### Observed Scope

<!-- Author prompt: Record the affected targets and when the impact was observed, with actual timestamps and their timezone. Derive any current lifecycle label from frontmatter status; do not keep a second current-state value or invent precision. -->

{{OBSERVED_SCOPE}}

#### Response

##### Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

##### Actions

<!-- Author prompt: Add one row per action actually taken and keep the table without rows until one is. Owner names who acted or says it is unrecorded; Evidence names a record or `none`. -->

| Action | Owner | Condition | Evidence |
| --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{CONDITION}} | {{EVIDENCE}} |

#### Resolution

##### Verified State

{{VERIFIED_STATE}}

##### Remaining Work

<!-- Author prompt: Record tracked next actions and their owners; move causal analysis and durable follow-up to the postmortem after stabilization. -->

{{REMAINING_WORK}}

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
