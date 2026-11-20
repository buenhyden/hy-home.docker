---
title: "Postflight Routing"
version: "2.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Postflight Routing
  layer: agent
updated: "2026-11-20"
---

# Postflight Routing

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

Route completion verification to the actual changed authority surface.

###### Authority
<!-- core-payload-level:4 -->

This policy is the canonical owner of completion verification routing for changed authority surfaces under [bootstrap precedence](bootstrap.md#authority-and-precedence).

##### Applies To

Completion verification selected for the changed canonical and protected surfaces.

###### Exclusions
<!-- core-payload-level:4 -->

None: this document states no exclusion.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POSTFLIGHT-CHECKLIST-R1 | Completion of a change | Required: record completion evidence in the co-located Stage 03 Task | none | co-located Stage 03 Task |
| POSTFLIGHT-CHECKLIST-R2 | Completion of a change | Required: treat Git history as the recovery boundary | none | none |
| POSTFLIGHT-CHECKLIST-R3 | Always | Forbidden: creating a second handoff or progress authority | none | none |
| POSTFLIGHT-CHECKLIST-R4 | Approved all-files gate | Required: leave direct pre-commit prohibition and every wrapper condition to `quality-standards.md#4-execution-boundary` | none | none |
| POSTFLIGHT-CHECKLIST-R5 | Approved all-files gate | Required: postflight records only the concise result and hook-managed fallout | none | none |

Completion evidence belongs in the co-located Stage 03 Task. Git history is the
recovery boundary. Do not create a second handoff or progress authority.

For an approved all-files gate, the
[execution boundary](../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary) owns direct
pre-commit prohibition and every wrapper condition. Postflight records only
the concise result and hook-managed fallout; the controlled wrapper reports
exit 20 for unexpected paths.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

No exception is granted here; a separately authorized operation follows [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md).

###### Approval and Review
<!-- core-payload-level:4 -->

None: no exception exists to approve.

#### Enforcement

##### Mechanisms

`task-checklists.md` is the completion authority. Apply only validators mapped
to the changed canonical source and protected surface. For provider projections,
run the agent governance contract and renderer check; write mode is used only through
the registered renderer.

##### Limits

Postflight routes to other owners and ties no check to any rule in Requirements.

- Evidence placement and handoff authority (R1-R3): no check is named.
- All-files gate (R4-R5): no check is named.
- Rules stated under Enforcement (Mechanisms) are outside this table.

#### Ownership

##### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records)).

##### Review Triggers

Changes land in place with Task evidence; related documents:

- [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md)
- [Quality standards](../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary)
- [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md)
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
