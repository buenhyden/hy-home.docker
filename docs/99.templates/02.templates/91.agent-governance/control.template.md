---
title: '{{TITLE}}'
version: 0.1.0
type: governance/policy
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: agent
updated: '{{UPDATED}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

Readers use the policy payload below for this document's information and judgments.

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

#### Purpose and Scope

##### Objective

<!-- Author prompt: State the control's purpose and link the bootstrap policy and the owning policy that give it authority. -->

{{CONTROL_PURPOSE_AND_AUTHORITY_LINKS}}

##### Applies To

<!-- Author prompt: Name the surfaces and actors under this control and those outside it. -->

{{SURFACES_ACTORS_AND_EXCLUSIONS}}

#### Rules

##### Requirements

<!-- Author prompt: List each rule in the table: Rule ID is a stable identifier within this policy, Condition when it applies, Requirement starting with "Required:", "Forbidden:" (the forbidden act, never a negated sentence) or "Allowed:", Enforcement a check only where the policy ties it to that rule, "manual" only where the policy says the rule rests on review, otherwise "none", and Evidence a record only where the policy says it confirms that rule, otherwise "none". One row per rule statement under Requirements and its subsections. Detail follows the table. -->

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| {{RULE_ID}} | {{CONDITION}} | {{REQUIREMENT}} | {{ENFORCEMENT}} | {{EVIDENCE}} |

{{REQUIRED_AND_PROHIBITED_BEHAVIOR}}

##### Exceptions

<!-- Author prompt: Name the scoped exceptions and the authorization boundary that approves them; write "None" when there is none. -->

{{SCOPED_EXCEPTIONS_AND_AUTHORIZATION}}

#### Enforcement

##### Mechanisms

<!-- Author prompt: Name the scoped checks, their expected signals, and the limits of what that evidence proves. -->

{{CHECKS_SIGNALS_AND_EVIDENCE_LIMITS}}

##### Limits

<!-- Author prompt: Name what is not mechanically enforced: rules that rest on review, provider behavior, or no check at all. -->

{{UNENFORCED_PARTS}}

#### Ownership

##### Owner

{{OWNER_AND_ENFORCING_ROLES}}

##### Review Triggers

{{WHEN_AND_HOW_THIS_POLICY_CHANGES_AND_RELATED_DOCUMENTS}}

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
