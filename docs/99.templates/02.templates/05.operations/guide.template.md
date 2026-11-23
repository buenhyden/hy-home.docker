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

<!-- 작성 규칙: 이 문서로 해결할 정보 필요와 실제 독자를 밝힌다. 본문 정책을 중복 복사하지 않는다. -->

Readers use the guide payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: 유지할 대상·적용과 제외 범위·책임자를 밝힌다. 메타데이터 자체가 실행 승인이나 인수 권한을 부여하지 않는다. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 실제로 존재하거나 명시적으로 생성할 입력, 제약, 전제를 구분한다. 확인한 사실과 가정을 혼동하지 않는다. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: 해당 kind의 payload와 조건·표·필드 의미를 소유한다. 관련 없는 문서 역할과 Release 책임을 모든 문서에 복제하지 않는다. -->

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

<!-- 작성 규칙: 실제 독자가 문서 또는 연결된 native 출력을 사용하는 방법을 설명한다. 필요 없는 운영·승인 단계를 만들지 않는다. -->

Use the procedures or reading order stated in the role payload.

### 확인 기준

<!-- 작성 규칙: 문서 목적에 필요한 확인만 제시한다. 설계·구현·검증·사용자 인수를 구별하고 모든 문서에 코드 시험을 강요하지 않는다. -->

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 정본 owner와 필요한 의존 관계의 목적을 적는다. 모든 문서의 양방향 링크나 과거 별칭을 강제하지 않는다. -->

The role payload retains the current owner and dependency references.

### 외부 근거

<!-- 작성 규칙: 외부 사실과 현재 설계의 적용·제외 이유를 구분한다. 출처가 실행 권한이나 성공 증거를 대신하지 않는다. -->

External basis and its limits remain those stated in the role payload; a citation grants no authority.
