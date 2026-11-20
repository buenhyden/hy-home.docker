---
title: '{{TITLE}}'
version: 0.1.0
type: common/agent-guide
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

Readers use the agent-guide payload below for this document's information and judgments.

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
<!-- Author prompt: Route to canonical owners; do not copy a policy, role, or skill body into this file. -->

#### Scope

##### Allowed Scope

<!-- Author prompt: Name the folder's purpose, the paths an agent may change below it, and what is out of scope. -->

{{ALLOWED_SCOPE_AND_NON_GOALS}}

##### Instruction Precedence

<!-- Author prompt: Say that when this guide and the owner of a rule it summarizes disagree, the owner wins and the guide is corrected, and link the bootstrap precedence order; never add a rank of your own. -->

{{INSTRUCTION_PRECEDENCE}}

#### Workflow

##### Intake

<!-- Author prompt: Link the `.agents/` policies, roles, skills, prompts and hook rules, and the `.claude/` and `.codex/` adapters and hooks an agent loads before working here. -->

{{CANONICAL_SOURCES}}

##### Execution

<!-- Author prompt: List the folder-specific steps and obligations an agent follows while changing a file here. -->

{{INSPECT_CHANGE_AND_LOCAL_OBLIGATIONS}}

#### Boundaries

##### Authority

<!-- Author prompt: Say when an agent stops and reports, and which approval owner decides; this guide grants no tool, path, permission or approval. -->

{{STOP_AND_ESCALATE}}

##### Secrets and External Effects

<!-- Author prompt: Name the protected actions: secret handling, generated files, live or remote effects and the approval each needs. -->

{{PROTECTED_ACTIONS}}

#### Verification

##### Checks

<!-- Author prompt: Name only registered commands that exist. -->

{{REQUIRED_CHECKS}}

##### Reporting

<!-- Author prompt: Say where check evidence and handoff state are recorded, what the checks do not prove, and link the human-facing documents. -->

{{EVIDENCE_LIMITS_AND_HANDOFF}}

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
