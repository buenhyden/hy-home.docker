---
title: "WARNING: non-Conventional Commit message"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: non-Conventional Commit message'
  layer: agent
updated: "2026-11-20"
action: "warn"
enabled: true
event: "bash"
name: "warn-conventional-commit"
pattern: "git\\s+commit(?!.*--amend|.*-C[\\s=])(?:(?!\\s-[A-Za-z]*m\\s).)*\\s-[A-Za-z]*m\\s+(\"|\\')(?!(build|chore|ci|deps|docs|feat|fix|perf|refactor|release|revert|style|test)(\\([^)]*\\))?!?:[ \\t]|Merge\\s|Revert\\s|Initial commit)"
---

# WARNING: non-Conventional Commit message

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

Apply the declared `warn` action for warn-conventional-commit.

##### Authority

Owning policy: [Git workflow](../../../docs/00.workspace/03.process/git-workflow.md).

#### Scope

##### Applies To

The `warn-conventional-commit` rule applies on the `bash` event and matches Bash commands that match its `pattern` ("WARNING: non-Conventional Commit message"). The frontmatter owns the exact matcher.

##### Exclusions

**Exclusions:** `--amend`, `-C` (message reuse), `Merge`, `Revert`, `Initial commit`

#### Rules

##### Requirements

**Non-Conventional Commit message detected (project rule)**

The message does not follow Commit Standards in
`docs/00.workspace/03.process/git-workflow.md`.

**Required format:**

```text
<type>[(scope)][!]: <description>
```

Allowed types are the keys in `.cz.toml`'s `change_type_map`. This warning's
pattern is a lightweight translation of that map. The installed `commit-msg`
hook checks the complete grammar when its delivery is observed. Use explicit
Commitizen validation when that delivery is unconfirmed or diagnosis is needed.
The remote candidate checks its authenticated contributor range.

**Correct examples:**

```bash
git commit -m "feat(nginx): Add rate limiting config"
git commit -m "fix(compose): Correct volume mount path"
git commit -m "docs(readme): Update service list"
git commit -m "chore!: Drop support for legacy volume names"
git commit -m "deps(pre-commit): Update Commitizen hook"
git commit -m "release: Publish v1.0.0"
```

**This rule detects:**

- `"Update something"`, `"Fix the bug"`, `"Add feature"` — missing type prefix
- `"feat something"` — missing colon separator
- `"FEAT: something"` — uppercase type

Reference issue IDs, ADR IDs, or plan/task IDs in the footer when applicable.

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
