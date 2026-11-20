---
title: "WARNING: branch naming rule violation"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: branch naming rule violation'
  layer: agent
updated: "2026-11-20"
action: "warn"
enabled: true
event: "bash"
name: "warn-branch-naming"
pattern: "git\\s+(checkout\\s+-b|switch\\s+-c)\\s+(?!(build|chore|ci|deps|docs|feat|fix|hotfix|perf|refactor|release|revert|style|test|renovate|codex)/)"
---

# WARNING: branch naming rule violation

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

Apply the declared `warn` action for warn-branch-naming.

##### Authority

Owning policy: [Git workflow](../../../docs/00.workspace/03.process/git-workflow.md).

#### Scope

##### Applies To

The `warn-branch-naming` rule applies on the `bash` event and matches Bash commands that match its `pattern` ("WARNING: branch naming rule violation"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Branch naming rule violation detected (project rule)**

The branch name does not follow the Branching Strategy in
`docs/00.workspace/03.process/git-workflow.md`.

**Allowed prefixes:**

| prefix | Purpose |
| ------ | ------- |
| `feat/[<issue-id>-]<description>` | new feature |
| `fix/[<issue-id>-]<description>` | bug fix |
| `hotfix/<description>` | urgent production fix |
| `<type>/<description>` | any other type admitted by `.cz.toml` |
| `renovate/**`, `codex/**` | automation-owned branches |

**Correct examples:**

```bash
git checkout -b feat/42-add-nginx-service
git checkout -b fix/17-fix-volume-mount
git checkout -b hotfix/patch-secret-leak
git checkout -b feat/add-nginx-service
git checkout -b deps/update-python-pins
git checkout -b release/publish-v1.0.0
```

Do not work directly on `main`. Start from a feature or fix branch.

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
