---
title: '{{TITLE}}'
version: 0.1.0
type: sdlc/architecture-decision
status: proposed
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

Readers use the architecture-decision payload below for this document's information and judgments.

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
<!-- Author prompt: Record one decision. State facts and the decision's authority only from evidence; never infer approval from the document's status alone. -->

#### Context

##### Problem and Drivers

<!-- Author prompt: State the problem and its drivers, and link the requirements, external sources and related architecture this decision rests on. -->

{{PROBLEM_DRIVERS_AND_CONSTRAINTS}}

##### Decision Scope

<!-- Author prompt: Name what the decision covers, what it leaves out, and the consumers it affects. -->

{{DECISION_SCOPE_AND_AFFECTED_CONSUMERS}}

#### Options

##### Considered Options

{{OPTIONS_ACTUALLY_CONSIDERED}}

##### Trade-offs

<!-- Author prompt: List every option in this table, the chosen one included: Option names it, Benefit its advantage, Cost and Risk what it costs or risks, and Reason why it was chosen or not. Detail follows the table. -->

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| {{OPTION}} | {{BENEFIT}} | {{COST_AND_RISK}} | {{REASON}} |

{{BENEFITS_RISKS_COSTS_AND_REASONS_NOT_CHOSEN}}

#### Decision

##### Chosen Option

{{CHOSEN_OPTION_CONDITIONS_AND_NORMATIVE_OWNER}}

##### Authority and Effect

<!-- Author prompt: Name who decided, the approval evidence, and when the decision takes effect. Write "not recorded" for a fact the record does not hold. When this decision supersedes, amends or is superseded by another, summarize it here under a Supersession heading; historical links are non-authoritative. -->

{{DECIDER_APPROVAL_EVIDENCE_AND_EFFECTIVE_DATE}}

#### Consequences

##### Impacts

{{IMPLEMENTATION_OPERATIONS_AND_QUALITY_IMPACTS}}

##### Follow-up

<!-- Author prompt: Name the follow-up work, how compliance is verified, and who owns each item. An owner-directed in-place amendment records its date and direction here. -->

{{FOLLOW_UP_VERIFICATION_AND_OWNERS}}

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
