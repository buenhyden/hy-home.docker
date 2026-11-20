---
title: '{{TITLE}}'
version: 0.1.0
type: reference/data
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
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

Readers use the data-reference payload below for this document's information and judgments.

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

#### Purpose

##### Consumers

<!-- Author prompt: Name who uses this data and for what. -->

{{CONSUMERS}}

##### Boundaries

<!-- Author prompt: State what this data is not authority for. -->

{{NON_AUTHORITY_BOUNDARIES}}

#### Provenance

##### Collection

<!-- Author prompt: Name the inputs and the generator or method that produced the data. -->

{{INPUTS_AND_GENERATOR}}

##### Versions and Dates

<!-- Author prompt: Give the input versions and the observation and generation dates. -->

{{INPUT_VERSIONS_AND_DATES}}

#### Interpretation

##### Schema and Units

<!-- Author prompt: List each field in the table: Field its name, Type its value type, Unit its unit or "none", Meaning what it means, and Limits its precision, missing values or cost. -->

| Field | Type | Unit | Meaning | Limits |
| --- | --- | --- | --- | --- |
| {{FIELD}} | {{TYPE}} | {{UNIT}} | {{MEANING}} | {{LIMITS}} |

##### Limits

<!-- Author prompt: State the range, constraints, refresh trigger and known errors of the data. -->

{{DATA_LIMITS}}

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
