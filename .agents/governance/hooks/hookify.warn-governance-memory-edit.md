---
title: "WARNING: canonical governance root authority edit"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: canonical governance root authority edit'
  layer: agent
updated: "2026-11-20"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)(\\.agents/README\\.md|docs/00\\.workspace/02\\.process/sdlc\\.md)$"
enabled: true
event: "file"
name: "warn-governance-memory-edit"
---

# WARNING: canonical governance root authority edit

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the rule payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

##### Objective

Apply the declared `warn` action for warn-governance-memory-edit.

##### Authority

Watched authorities: `.agents/README.md` (governance inventory) and `docs/00.workspace/03.process/sdlc.md`.

#### Scope

##### Applies To

The `warn-governance-memory-edit` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: canonical governance root authority edit"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Canonical governance root authority edit detected**

Confirm that the change preserves the registered canonical governance inventory, routes
document shapes to Stage 99, records evidence in the co-located Task, and
regenerates provider projections when their inputs change.

##### Enforcement

Native event delivery is a separate observation from the frontmatter match.

#### Exceptions

##### Exception Conditions

No exception is declared by this rule.

##### Approval and Review

None.

#### Ownership

##### Responsibilities

`@buenhyden`.

##### Change and Adoption

None.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
