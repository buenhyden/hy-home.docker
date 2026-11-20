---
title: "WARNING: Stage document edit"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: Stage document edit'
  layer: agent
updated: "2026-11-20"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/(0[1-9]|[1-9][0-9])\\."
enabled: true
event: "file"
name: "warn-stage-doc-edit"
---

# WARNING: Stage document edit

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

Apply the declared `warn` action for warn-stage-doc-edit.

##### Authority

Owning policy: [Agent Bootstrap Policy](../bootstrap.md#hard-constraints).

#### Scope

##### Applies To

The `warn-stage-doc-edit` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: Stage document edit"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Stage document edit detected (project rule)**

`docs/01` through `docs/99` are **read-only by default**.

**Canonical bootstrap policy (`bootstrap.md#hard-constraints`):**
> "Stage documents are read-only unless the request authorizes change."

**Before editing, confirm:**

- [ ] The user explicitly authorized the stage document edit.
- [ ] The target is inside an active stage artifact directory (the stages listed in [stage-authoring-matrix.md](../../../docs/00.workspace/01.project/stage-authoring-matrix.md)).
- [ ] The edit is in-place; no parallel replacement file is being created.
- [ ] This rule applies whether the path arrives as `docs/...` or `/.../docs/...`.

**After editing, inspect the selected plan:**

```bash
python3 scripts/validation/run-ci-gate.py --profile changed --explain
```

The plan inspection does not execute QA. Follow the current
[quality policy](../../../docs/00.workspace/04.quality/quality-standards.md#canonical-delivery-phase-matrix) for
focused authoring checks and remote PR candidate validation.

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
