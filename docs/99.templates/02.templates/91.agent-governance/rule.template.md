---
title: '{{TITLE}}'
version: 0.1.0
type: governance/rule
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: agent
updated: '{{UPDATED}}'
action: warn
enabled: true
event: '{{EVENT}}'
name: '{{NAME}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the rule payload below for this document's information and judgments.

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

#### Purpose

##### Objective

{{WHY_THIS_RUNTIME_RULE_EXISTS}}

##### Authority

{{OWNING_POLICY_LINK}}

#### Scope

##### Applies To

{{RULE_NAME_EVENT_AND_MATCHING_SCOPE}}

##### Exclusions

{{EVENTS_AND_PATHS_THE_RULE_DOES_NOT_MATCH}}

#### Rules

##### Requirements

{{MESSAGE_SHOWN_WHEN_THE_RULE_FIRES}}

##### Enforcement

{{DECLARED_ACTION_AND_MATCHING_SCOPE_CHECKS}}

#### Exceptions

##### Exception Conditions

{{APPROVED_ALTERNATIVE_ACTION}}

##### Approval and Review

{{WHO_APPROVES_AN_EXCEPTION}}

#### Ownership

##### Responsibilities

{{RULE_OWNER_AND_PARITY_OWNER}}

##### Change and Adoption

{{HOW_THE_RULE_CHANGES_AND_PARITY_LINKS}}

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
