---
title: "WARNING: Korean text in governance documentation"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: Korean text in governance documentation'
  layer: agent
updated: "2026-11-20"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)((?:\\.agents|docs/00\\.workspace)/(?:[^/]+/)*(?!README\\.md$)[^/]+\\.md|\\.(claude|codex)/provider\\.md)$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "[\\uac00-\\ud7a3\\u3131-\\u318e]"
enabled: true
event: "file"
name: "warn-korean-in-governance"
---

# WARNING: Korean text in governance documentation

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

Apply the declared `warn` action for warn-korean-in-governance.

##### Authority

Owning policy: `docs/00.workspace/03.process/documentation-protocol.md`.

#### Scope

##### Applies To

The `warn-korean-in-governance` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("WARNING: Korean text in governance documentation"). The frontmatter owns the exact matcher.

##### Exclusions

It skips `README.md` files, whose language the documentation protocol owns; the negative lookahead in the path pattern is what excludes them, so keep it when editing the pattern.

#### Rules

##### Requirements

**Korean text detected in governance documentation (project rule)**

This hook is an advisory detector. Resolve the file's language through the sole
document-role authority at
`docs/00.workspace/03.process/documentation-protocol.md#document-language`;
the hook does not publish a second language table or exception rule.

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

`.agents/README.md`.

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
