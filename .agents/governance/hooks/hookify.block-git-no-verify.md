---
title: "BLOCKED: git commit --no-verify"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: git commit --no-verify'
  layer: agent
updated: "2026-11-20"
action: "block"
enabled: true
event: "bash"
name: "block-git-no-verify"
pattern: "git\\s+commit\\s+.*(--no-verify|-n\\s+-m|-n\\s+['\"]|-n$)"
---

# Git Commit Check Bypass Rule

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

**`git commit --no-verify` blocked (project rule)**

##### Authority

Owning policies:

- [Git workflow](../../../docs/00.workspace/03.process/git-workflow.md)
- [Quality standards execution boundary](../../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary)

#### Scope

##### Applies To

The `block-git-no-verify` rule applies on the `bash` event. `docs/00.workspace/03.process/git-workflow.md` — Enforcement:

> "Changes that bypass checks or violate secret safety must not be merged."

The [execution boundary](../../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary) owns the
direct pre-commit prohibition and the sole approved all-files route. This hook
retains the separate block on bypassing configured commit checks.

##### Exclusions

None.

#### Rules

##### Requirements

**Project pre-commit hooks perform:**

- lint and format checks
- plaintext secret detection
- file type and size checks

**Why this rule blocks:**

- Bypassing pre-commit skips quality and security gates.
- Accidental secret commits become more likely.
- CI may block the PR on lint failures.

**Correct approach:**

```bash
# BLOCKED: git commit --no-verify
git commit --no-verify -m "fix: Something"
git commit -n -m "fix: Something"

# If hooks fail, fix the root cause.
# Lint error: edit the affected file directly.
# Format error: apply the formatter, then stage the result.
git add -p
git commit -m "fix(scope): Actual fix"
```

##### Enforcement

The declared Bash event and unchanged native pattern identify matching commands.

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
