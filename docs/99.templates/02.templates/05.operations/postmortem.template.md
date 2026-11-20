---
title: '{{TITLE}}'
version: 0.1.0
type: operation/postmortem
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
layer: operations
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

Readers use the postmortem payload below for this document's information and judgments.

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
<!-- Author prompt: When the postmortem is reviewed, add optional `reviewed_at` after `created`. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

#### Facts

##### Timeline

<!-- Author prompt: Name the incident and the reviewed period, then the events with their recorded timestamps. -->

{{TIMELINE}}

##### Impact

{{IMPACT}}

#### Causes

##### Contributing Factors

<!-- Author prompt: Record only verified causes and the conditions that let them act; avoid blame. -->

{{CONTRIBUTING_FACTORS}}

##### Uncertainty

{{UNCERTAINTY}}

#### Actions

##### Prevention

{{PREVENTION}}

##### Owners and Checks

<!-- Author prompt: Each action needs an owner, the condition that completes it and the evidence that checks it; Evidence names the tracking record or link and the check; `none` only for a lesson row with no corrective action. Do not set a completion deadline. -->

| Action | Owner | Condition | Evidence |
| --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{CONDITION}} | {{EVIDENCE}} |

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
