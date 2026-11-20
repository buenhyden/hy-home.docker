---
title: "WARNING: template use required"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: template use required'
  layer: agent
updated: "2026-11-20"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/(0[1-5]|90)\\."
enabled: true
event: "file"
name: "enforce-docs-templates"
---

# WARNING: template use required

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

Apply the declared `warn` action for enforce-docs-templates.

##### Authority

Owning policies:

- [Documentation protocol](../../../docs/00.workspace/03.process/documentation-protocol.md)
- [Stage authoring matrix](../../../docs/00.workspace/01.project/stage-authoring-matrix.md)

#### Scope

##### Applies To

The `enforce-docs-templates` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: template use required"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Template use required (project rule)**

When creating or editing documents under `docs/01` through `docs/05` or
`docs/90`, follow the mapped template under `docs/99.templates/02.templates/`.

The canonical `docs/00.workspace/03.process/documentation-protocol.md` authoring rules
require selecting the Stage 99 profile and preserving its metadata, links, and
stage-specific contract. The Registry owns the mapped template for each profile.

**Required actions:**

1. Read the mapped template under `docs/99.templates/02.templates/` before editing.
2. Preserve required heading structure.
3. Remove all temporary placeholders before saving.
4. Keep related links in the section the template declares for them, such as
   `Traceability` or `References` for a role on the common form and
   `## Related Documents` for a role that has not moved.

After editing, inspect `python3 scripts/validation/run-ci-gate.py --profile changed --explain`.
This selects checks without executing or accepting template validation.

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
