---
title: "AI Agent Identity Routing"
version: "2.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: AI Agent Identity Routing
  layer: agent
updated: "2026-11-20"
---

# AI Agent Identity Routing

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Resolve a single canonical role identity before repository work.

###### Authority
<!-- core-payload-level:4 -->

This policy is the canonical owner of canonical role identity resolution before repository work under [bootstrap precedence](bootstrap.md#authority-and-precedence).

##### Applies To

Canonical role selection and provider-neutral identity before repository mutation.

###### Exclusions
<!-- core-payload-level:4 -->

None: this document states no exclusion.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| PERSONA-R1 | Before repository mutation | Required: resolve exactly one canonical `agent_id` from `.agents/roles/` | none | none |
| PERSONA-R2 | Before repository mutation | Required: use the resolved role's scope, permission profile, work profile and skill IDs | none | none |
| PERSONA-R3 | Before repository mutation | Forbidden: inventing a provider-local identity | none | none |
| PERSONA-R4 | Always | Required: provider-native adapters preserve role intent | none | none |
| PERSONA-R5 | Always | Forbidden: provider-native adapters owning names, permissions or model policy | none | none |
| PERSONA-R6 | No role matches or multiple roles conflict | Required: stop and route the ambiguity to `workflow-supervisor` | none | none |
| PERSONA-R7 | Multi-role work | Required: keep one supervising owner | none | none |
| PERSONA-R8 | High-risk multi-role work | Required: separate implementation from independent review | none | none |

Before mutation, resolve exactly one canonical `agent_id` from `.agents/roles/`. Use its
scope, permission profile, work profile, and skill IDs without inventing a
provider-local identity. Provider-native adapters preserve role intent but do
not own names, permissions, or model policy.

If no role matches or multiple roles conflict, stop and route the ambiguity to
`workflow-supervisor`. Multi-role work keeps one supervising owner and, for
high-risk work, separates implementation from independent review.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

No exception is granted here; a separately authorized operation follows [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md).

###### Approval and Review
<!-- core-payload-level:4 -->

None: no exception exists to approve.

#### Enforcement

##### Mechanisms

None: this document states no separate check.

##### Limits

This policy states no separate check, so none of its rules is mechanically enforced:

- Role identity and adapter limits: R1-R5.
- Ambiguity routing: R6.
- Multi-role ownership and review separation: R7-R8.

#### Ownership

##### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records)).

##### Review Triggers

Changes land in place with Task evidence; related documents:

- [Bootstrap policy](bootstrap.md)
- [Agentic policy](agentic.md)
- [Roles](../roles/)
- [Provider registry](providers/registry.yaml)

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
