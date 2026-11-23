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

<!-- 작성 규칙: 이 문서로 해결할 정보 필요와 실제 독자를 밝힌다. 본문 정책을 중복 복사하지 않는다. -->

Readers use the plan payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: 유지할 대상·적용과 제외 범위·책임자를 밝힌다. 메타데이터 자체가 실행 승인이나 인수 권한을 부여하지 않는다. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 실제로 존재하거나 명시적으로 생성할 입력, 제약, 전제를 구분한다. 확인한 사실과 가정을 혼동하지 않는다. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: 해당 kind의 payload와 조건·표·필드 의미를 소유한다. 관련 없는 문서 역할과 Release 책임을 모든 문서에 복제하지 않는다. -->

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
