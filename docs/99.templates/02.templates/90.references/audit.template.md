---
title: '{{TITLE}}'
version: 0.1.0
type: reference/audit
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: reference
updated: '{{UPDATED}}'
layer: references
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

Readers use the audit payload below for this document's information and judgments.

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

#### Scope

##### Subject

<!-- Author prompt: Name the claim or surface audited and the criteria it is held to. -->

{{AUDIT_SUBJECT_AND_CRITERIA}}

##### Read Coverage

<!-- Author prompt: Name what was actually read or run, at which revision, and what was not. -->

{{READ_AND_RUN_COVERAGE}}

#### Findings

##### Evidence

<!-- Author prompt: List each finding in the table: Finding ID a stable identifier within this member, Requirement the current obligation, Evidence what was directly checked, Classification one of confirmed, gap, conflict, unverified or not-applicable, Action the concrete fix, Owner who does it, and Acceptance the condition that closes it. -->

| Finding ID | Requirement | Evidence | Classification | Action | Owner | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |
| {{FINDING_ID}} | {{REQUIREMENT}} | {{EVIDENCE}} | {{CLASSIFICATION}} | {{ACTION}} | {{OWNER}} | {{ACCEPTANCE}} |

##### Conflicts and Gaps

<!-- Author prompt: Explain each conflict or gap between claim and evidence and its impact. -->

{{CONFLICTS_AND_GAPS}}

#### Actions

##### Owners

<!-- Author prompt: Name the current work and its owner for each finding that needs action. -->

{{OWNERS}}

##### Acceptance Conditions

<!-- Author prompt: State the evidence that closes each action. -->

{{ACCEPTANCE_CONDITIONS}}

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
