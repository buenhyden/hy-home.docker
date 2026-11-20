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

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the architecture-description payload below for this document's information and judgments.

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
