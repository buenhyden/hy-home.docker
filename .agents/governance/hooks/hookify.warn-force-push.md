---
title: "Prefer --force-with-lease over --force."
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Prefer --force-with-lease over --force.
  layer: agent
updated: "2026-11-20"
action: "warn"
enabled: true
event: "bash"
name: "warn-force-push"
pattern: "git\\s+push\\s+.*(--force\\b|--force-with-lease\\b|-f\\s|-f$)"
---

# Prefer --force-with-lease over --force

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

Apply the declared `warn` action for warn-force-push.

##### Authority

Owning policy: [GitHub governance](../../../docs/00.workspace/03.process/github-governance.md).

#### Scope

##### Applies To

The `warn-force-push` rule applies on the `bash` event and matches Bash commands that match its `pattern` ("Prefer --force-with-lease over --force."). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Force push detected (project rule)**

`docs/00.workspace/03.process/github-governance.md` — Repository Protection Contract:

> "no direct pushes, no force pushes, no bypass of required checks"

**When a force push may be justified:**

- Rewriting history after a rebase on your own feature branch.
- Using `--force-with-lease` to protect against overwriting remote changes.

**Never allowed:**

- Force pushing to `main`.
- Force pushing another agent's or developer's in-progress branch.
- Force pushing commits that have already been merged.

**Confirmation checklist:**

- [ ] This is your own branch, not `main`.
- [ ] The command uses `--force-with-lease`, not plain `--force`.
- [ ] No teammate or agent is working on the same branch.

```bash
# Prefer --force-with-lease over --force.

git push --force-with-lease origin feat/42-my-feature
```

##### Enforcement

Native event delivery is a separate observation from the frontmatter match.

#### Exceptions

##### Exception Conditions

Own feature branch after rebase, with `--force-with-lease` (see Requirements).

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
