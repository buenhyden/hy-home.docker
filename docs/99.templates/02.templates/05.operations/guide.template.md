---
title: '{{TITLE}}'
version: 0.1.0
type: operation/guide
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

Readers use the guide payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: Name the maintained subject, scope and owner; do not grant authority through document metadata. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: State actual inputs, constraints or preconditions, and distinguish facts from assumptions. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: Keep the kind-specific payload here with its conditions, tables and one canonical responsibility. -->

<!-- Author prompt: Service Guides add optional `implementation_services` frontmatter as a mapping from each repo-relative active Compose path to its nonempty list of owned service names; workspace and process Guides omit it. -->

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

#### Purpose

##### Audience

<!-- Author prompt: Name who reads this guide and for what task; use only readers the subject and its owners actually have. -->

{{READERS_AND_THEIR_TASK}}

##### Outcome

<!-- Author prompt: State the goal and the primary tutorial, how-to, reference or explanation need, what this guide covers and leaves out, and link the implementation, requirement and policy that own the subject. -->

{{READER_GOAL_SCOPE_AND_AUTHORITY_LINKS}}

#### Prerequisites

##### Environment

{{IMPLEMENTATION_ENVIRONMENT_AND_CONCEPTS}}

##### Authority

<!-- Author prompt: Name the access, approvals and secret names (never values) the reader needs; write "none" when nothing is required. -->

{{ACCESS_APPROVALS_AND_SECRET_NAMES}}

#### Procedure

##### Steps

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. Identify the actual implementation and Compose ownership, service profiles and HOME/DEV/OPTIONAL/LAB classification, network and exposure, data and persistence, dependencies, environment and secret names (never values), resources, security and authentication, normal use, backup prerequisites and recovery, upgrade and migration, observable readiness, and official sources. For a non-service workspace subject, keep only the fields its implementation actually has. Route executable maintenance and recovery to the Runbook; do not duplicate its commands. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

<!-- Author prompt: When the procedure is an ordered sequence, list it in this table: Step is its number, Action the permitted action, Expected Result what to observe, and On Failure where to stop and who takes over. Otherwise delete the table. Special cases and limits follow the table. -->

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| {{STEP}} | {{ACTION}} | {{EXPECTED_RESULT}} | {{ON_FAILURE}} |

{{NORMAL_USE_ACTIONS_SPECIAL_CASES_AND_LIMITS}}

##### Expected Results

{{COMMON_CHECKS_AND_EXPECTED_RESULT}}

#### Troubleshooting

##### Symptoms

<!-- Author prompt: Give symptoms and diagnosis; when an actual runbook owns executable steps, link it without copying commands. -->

{{SYMPTOMS_AND_DIAGNOSIS}}

##### Next Action

<!-- Author prompt: Name where the reader goes next when the symptom persists: the runbook, owner or escalation the subject actually has. -->

{{RUNBOOK_OWNER_OR_ESCALATION}}

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
