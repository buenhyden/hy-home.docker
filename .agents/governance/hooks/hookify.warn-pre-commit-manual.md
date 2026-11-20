---
title: "WARNING: manual pre-commit execution"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: manual pre-commit execution'
  layer: agent
updated: "2026-11-20"
action: "warn"
enabled: true
event: "bash"
name: "warn-pre-commit-manual"
pattern: "pre-commit\\s+run"
---

# Manual Pre-commit Execution Warning

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

**Manual `pre-commit run` detected (project rule)**

##### Authority

Owning policy: [Quality standards execution boundary](../../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary).

#### Scope

##### Applies To

Bash commands matching the frontmatter pattern.

##### Exclusions

None.

#### Rules

##### Requirements

Agents never run `pre-commit run` directly. Use the observed installed hooks
for an ordinary commit. When installed delivery is unconfirmed or diagnosis is
needed, use `scripts/validation/run-ci-precommit.sh --mode local-staged`. Server
PR checks use the authenticated `--mode pr-merge` route.

**Project pre-commit policy:**

- Manual runs can create inconsistent evidence.
- Installed commit-hook delivery must be observed separately; this warning does
  not claim it ran automatically for a particular commit.
- Remote candidate validation uses the registered read-only changed-style
  controller; routine CI does not run an all-files formatter.

**Detected forms and normal commit path:**

```bash
# WARNING: manual pre-commit execution is prohibited for agents
pre-commit run --all-files
pre-commit run --files myfile.py

# Let the installed hooks check the reviewed index and message.
git commit -m "feat(scope): My change"
```

If lint or format issues exist, fix the affected files directly before committing.

##### Enforcement

The declared Bash event and unchanged native pattern identify matching commands.

#### Exceptions

##### Exception Conditions

An explicitly approved all-files gate uses only its controlled route and conditions.

##### Approval and Review

That gate needs explicit approval under the execution boundary.

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
