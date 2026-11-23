---
title: '{{TITLE}}'
version: 0.1.0
type: sdlc/architecture-description
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
layer: architecture
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

Readers use the architecture-description payload below for this document's information and judgments.

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
<!-- Author prompt: Describe the current structure only. Link decisions to their ADRs instead of restating them, and mark historical material as non-authoritative. -->

#### Context and Boundaries

##### System Boundary

<!-- Author prompt: State the purpose and readers, the system, version and environment boundary, and the external actors, neighbouring systems and data flows across it. -->

{{PURPOSE_BOUNDARY_ACTORS_AND_DATA_FLOWS}}

##### Constraints

{{REQUIREMENT_QUALITY_TECHNICAL_AND_SECURITY_CONSTRAINTS}}

#### Structure

##### Building Blocks

<!-- Author prompt: When a diagram shows the structure, review it against the [C4 diagram review checklist](https://c4model.com/diagrams/checklist). -->

{{COMPONENTS_RESPONSIBILITIES_AND_OWNERS}}

##### Interfaces

<!-- Author prompt: When the structure has an external interface, list it in this table: Interface is the boundary, Producer and Consumer its two sides, Contract a link to its input and output meaning, and Failure how a failure is handled. Otherwise delete the table. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| {{INTERFACE}} | {{PRODUCER}} | {{CONSUMER}} | {{CONTRACT}} | {{FAILURE}} |

{{INPUTS_OUTPUTS_CALLS_SCHEMAS_AND_COMPATIBILITY}}

#### Runtime Behavior

##### Normal Flow

{{RUNTIME_DEPLOYMENT_AND_ENVIRONMENT_DIFFERENCES}}

##### Failure and Recovery

{{FAILURE_RETRY_ISOLATION_AND_RECOVERY_BOUNDARIES}}

#### Quality Scenarios

##### Scenarios

{{QUALITY_SCENARIOS_RISKS_AND_OWNERS}}

##### Trade-offs

<!-- Author prompt: Name the quality trade-offs the structure accepts and what each one costs. -->

{{QUALITY_TRADE_OFFS}}

#### Decisions and Adoption

##### Decisions

{{EFFECTIVE_ADRS_AND_REASONS}}

##### Adoption Boundaries

<!-- Author prompt: Map the requirements and design constraints this structure meets, and state what is current, what it replaced and where history lives; historical links are non-authoritative. -->

{{REQUIREMENT_MAPPING_CURRENTNESS_AND_LINEAGE}}

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
