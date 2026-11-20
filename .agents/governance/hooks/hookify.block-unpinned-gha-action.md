---
title: "BLOCKED: floating reference"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: floating reference'
  layer: agent
updated: "2026-11-20"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "\\.github/workflows/.*\\.ya?ml$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "uses:\\s+\\S+@(latest|main|master|develop|dev)\\b"
enabled: true
event: "file"
name: "block-unpinned-gha-action"
---

# BLOCKED: floating reference

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

Apply the declared `block` action for block-unpinned-gha-action.

##### Authority

Owning policy: [GitHub governance](../../../docs/00.workspace/03.process/github-governance.md).

#### Scope

##### Applies To

The `block-unpinned-gha-action` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("BLOCKED: floating reference"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Floating GitHub Actions reference blocked (project rule)**

`docs/00.workspace/03.process/github-governance.md` — GitHub Actions Security Contract: the workflow uses a floating branch or tag reference.

**Detected pattern:** `uses: owner/action@latest` / `@main` / `@master` / `@develop`

**Why this is risky:**

- External actions can change without review.
- Floating refs increase supply-chain attack exposure.
- Builds are not reproducible.

**Safe alternative:**

```yaml
# BLOCKED: floating reference

- uses: actions/checkout@main
- uses: actions/setup-python@latest

# ALLOWED: pinned version or commit SHA
- uses: actions/checkout@v4.2.2
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Commit SHA pinning is safest. If a version tag is used, prefer digest verification.

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
