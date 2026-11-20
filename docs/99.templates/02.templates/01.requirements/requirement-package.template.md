---
title: '{{TITLE}}'
version: 0.1.0
type: sdlc/requirement
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
layer: requirements
artifact_id: '{{ARTIFACT_ID}}'
created: '{{CREATED}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the requirement payload below for this document's information and judgments.

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

#### Overview

##### Problem and Outcome

{{PROBLEM_AND_OUTCOME}}

##### Stakeholders

{{STAKEHOLDERS}}

#### Scope

##### In Scope

{{IN_SCOPE}}

##### Constraints and Exclusions

<!-- Author prompt: State constraints, assumptions, risks and non-goals. Write "None" with a reason when one does not apply. -->

{{CONSTRAINTS_AND_EXCLUSIONS}}

#### Requirements

<!-- Author prompt: List every FR and NFR in this table: Requirement ID is its full identity, Statement the needed behaviour or quality, Rationale why it is needed, Acceptance the judgeable condition, and Priority must, should or could. Statement repeats the declaration. Priority follows its modal verb: a declaration without one binds as must in an approved package. The declarations follow under their subsections; keep this table directly under Requirements so it is not read as a declaration. -->

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| {{REQUIREMENT_ID}} | {{STATEMENT}} | {{RATIONALE}} | {{ACCEPTANCE}} | {{PRIORITY}} |

<!-- Author prompt: When a quality requirement applies, measure each NFR in this table: Attribute is the quality characteristic, Measure the measurement definition, Unit its unit, Environment where it is measured, and Criterion the accepted value. Otherwise delete the table. -->

| Requirement ID | Attribute | Measure | Unit | Environment | Criterion |
| --- | --- | --- | --- | --- | --- |
| {{QUALITY_REQUIREMENT_ID}} | {{ATTRIBUTE}} | {{MEASURE}} | {{UNIT}} | {{ENVIRONMENT}} | {{CRITERION}} |

##### Functional Requirements

<!-- Author prompt: Give each requirement its rationale and priority. Write an interface need as a functional or quality requirement; no IF identity is issued. When interface references apply, add the optional frontmatter interface_refs map from declared full FR/NFR identities to scoped relative, fragment, HTTPS/HTTP or URN references. Do not require a future implementation target to exist or copy an executable contract here. -->

- **REQ-####-FR-####**: {{FUNCTIONAL_REQUIREMENT}}

##### Quality Requirements

<!-- Author prompt: Declare each quality requirement here; when none applies, say so and why. -->

- **REQ-####-NFR-#### — {{QUALITY_CHARACTERISTIC}}**: {{QUALITY_REQUIREMENT}}; measure: {{MEASURE_UNIT_ENVIRONMENT_AND_ACCEPTANCE}}

#### Traceability

##### Sources

<!-- Author prompt: Name the sources and governing constraints this package rests on. -->

{{SOURCES_AND_GOVERNING_CONSTRAINTS}}

##### Verification Links

<!-- Author prompt: State each acceptance condition, how it is judged, the evidence it needs and who decides, and link only existing architecture, Spec and verification documents. -->

{{ACCEPTANCE_VERIFICATION_AND_DOWNSTREAM_LINKS}}

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
