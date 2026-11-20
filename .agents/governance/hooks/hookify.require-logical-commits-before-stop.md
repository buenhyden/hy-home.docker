---
title: "BLOCKED: incomplete logical commits"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: incomplete logical commits'
  layer: agent
updated: "2026-11-20"
action: "block"
enabled: true
event: "stop"
name: "require-logical-commits-before-stop"
pattern: ".*"
---

# BLOCKED: incomplete logical commits

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

Apply the declared `block` action for require-logical-commits-before-stop.

##### Authority

Owning policy: [Git workflow](../../../docs/00.workspace/03.process/git-workflow.md#5-agent-completion-commit-discipline).

#### Scope

##### Applies To

The `require-logical-commits-before-stop` rule applies on the `stop` event and matches the end of an agent turn ("BLOCKED: incomplete logical commits"); [Enforcement](#enforcement) states how it is enforced.

##### Exclusions

None.

#### Rules

##### Requirements

**Logical commit completion check**

Before the final response for completed repository-modifying work:

- Inspect `git status --short` and the relevant diffs.
- Stage only files or hunks that belong to the current task.
- Create small Conventional Commits by logical unit after required checks pass.
- Leave unrelated untracked files untouched.
- If commits are intentionally skipped, state the reason clearly.

The shared Stop hook conservatively blocks on Git-visible uncommitted
changes. Git status does not establish which task or person owns a path,
nor does it grant permission to stage or commit it. Inspect ownership and
scope before acting, preserve unrelated changes, and use the applicable
incomplete-handoff route if completion cannot be established. The gate
does not replace review of the staged diff or waive required checks.

A repeated Stop payload (`stop_hook_active: true`) returns without another
block or verification run. The first attempt retains the uncommitted-change
check; a retry does not certify completion.

##### Enforcement

`scripts/hooks/hook_rules.py` does not evaluate `event: stop` rules; their `pattern: .*` is a placeholder. The enforcing code is `logical_commit_stop_gate` in `scripts/hooks/agent-event-hook.sh`. Native event delivery remains a separate observation.

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
