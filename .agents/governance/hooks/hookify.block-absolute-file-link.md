---
title: "BLOCKED: absolute file:// link"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: absolute file:// link'
  layer: agent
updated: "2026-11-20"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "\\.md$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "\\]\\(file://|href=[\"']file://"
enabled: true
event: "file"
name: "block-absolute-file-link"
---

# BLOCKED: absolute file:// link

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

Apply the declared `block` action for block-absolute-file-link.

##### Authority

No governance policy states the file:// ban; this rule owns it.

#### Scope

##### Applies To

The `block-absolute-file-link` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("BLOCKED: absolute file:// link"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Absolute `file://` link blocked (project rule)**

The document link contract and this hook require portable repository links.
Use a relative path instead of a machine-specific `file://` URL.

**Why this is forbidden:**

- `file://` links work only on one local machine.
- They break in CI, for other developers, and in GitHub rendering.
- They break SSoT traceability.

**Correct link format:**

```markdown
<!-- BLOCKED: absolute file URL -->
[document link](file:///home/hy/projects/hy-home.docker/docs/01.requirements/0001-gateway.md)

<!-- ALLOWED from inside docs/: relative link -->
[document link](../01.requirements/0001-gateway.md)

<!-- ALLOWED from outside docs/: entry point plus the path as text -->
[Documentation index](../../../docs/README.md) - `docs/01.requirements/0001-gateway.md`
```

Calculate relative paths from the current file location.

The declared action applies when the pattern matches.

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
