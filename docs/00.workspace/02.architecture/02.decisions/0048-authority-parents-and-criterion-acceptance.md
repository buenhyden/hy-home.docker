---
title: "Authority Parents and Criterion Acceptance"
version: "2.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0048"
parent_ids:
- "AD-0030"
created: "2026-10-13"
---

# ADR-0048: Authority Parents and Criterion Acceptance

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

Lifecycle generation 5 records execution state twice: a Task's frontmatter
`status`, and Spec and Plan statuses that must project it as `in-progress`,
`blocked` or `completed`. ADR-0037 decisions 1 to 3 make a `completed` Spec and
Plan the condition for a package to wait in Stage 03 and check completion
receipts built from per-row acceptance. On `main` `2a57d4122` the Evidence
column held 275 `accepted` and 275 `pending` rows, and a `FAIL` row with
`pending` acceptance blocked nothing. The prompt v9 request (findings F03 and
F06) asks for one owner for execution state, acceptance and readiness.

One writer per fact; no status copied between documents. Acceptance decided
once per criterion. Readiness computed, never stored. Frozen records keep the
meaning of the generation that wrote them.

###### Sources
<!-- core-payload-level:4 -->

- [AD-0030](../01.descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037](0037-package-disposition-wait-and-task-cancellation.md)
- SPEC-0231
- SPEC-0233

##### Decision Scope

This decision covers execution state, criterion acceptance and archive readiness for Spec, Plan and Task documents under lifecycle generation 6. It affects REQ-0026-FR-0009, AD-0030 and the ADR-0037 waiting rule, and leaves ADR-0037 decisions 4 onward unchanged.

#### Options

##### Considered Options

- Keep projected parent statuses and only relax the waiting rule: rejected;
  the duplicate execution state stays.
- Keep per-row acceptance and add an unresolved-`FAIL` check: rejected; a
  criterion would still carry several independent decisions.
- Defer the multi-item mode: rejected by the owner on 2026-10-13.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep projected parent statuses and only relax the waiting rule | The ADR records no benefit for this option. | The duplicate execution state stays. | Rejected; the duplicate execution state stays. |
| Keep per-row acceptance and add an unresolved-`FAIL` check | The ADR records no benefit for this option. | A criterion would still carry several independent decisions. | Rejected; a criterion would still carry several independent decisions. |
| Defer the multi-item mode | The ADR records no benefit for this option. | The ADR records no cost or risk for this option. | Rejected by the owner on 2026-10-13. |
| Authority-only Spec and Plan statuses, Task-owned execution state, one Criterion Acceptance row per criterion and derived readiness (chosen) | One writer per fact, acceptance decided once per criterion, and readiness computed rather than stored. | Lifecycle generation 6 adds a Registry migration and a Git-bound proof, and a branch still writing generation 5 Evidence must take the same rewrite. | Chosen from the owner's choice of these options to give one owner for execution state, acceptance and readiness (findings F03 and F06). |

Each rejected option is rejected for the reason stated in its entry above: projected parent statuses keep the duplicate execution state, per-row acceptance still carries several independent decisions per criterion, and deferring the multi-item mode was rejected by the owner on 2026-10-13.

#### Decision

##### Chosen Option

1. Spec and Plan statuses record authority only: `draft`, `in-review`,
   `approved`, `cancelled`, `superseded`. A Plan is never ahead of its Spec,
   and a Task or item runs only under an approved Spec and Plan.
2. A Task owns execution state: one frontmatter `status`, or, in a multi-item
   Task, one status per Execution Items row and no frontmatter `status`.
3. Evidence rows record observations and which earlier `FAIL` rows a `PASS`
   resolves. A criterion the Plan assigns to a current, non-cancelled Task has
   exactly one Criterion Acceptance row, in one such Task, recording
   `pending`, `accepted`, `rejected` or `not-required`; a criterion whose
   assigned Tasks are all historical or cancelled has none. `accepted` needs
   `PASS` evidence and no unresolved `FAIL`.
   A completed Task or item needs every criterion it decides for its work
   accepted or `not-required`.
4. A package is ready for archive review when its parents are `approved` (or
   validly `cancelled` or `superseded`), every Task or item is terminal, every
   criterion is accepted or `not-required`, and no `FAIL` is unresolved. A
   ready package with an approved Spec may wait in Stage 03; a cancelled or
   superseded Spec keeps no member there. A package enters the completed
   archive only from a ready base revision with an approved Spec, and the
   preserved copy keeps every base member with its status. Readiness is
   derived and is not disposition approval.

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. The Follow-up records that the owner accepted this decision on 2026-10-13. Effective from 2026-10-13.

###### Supersession
<!-- core-payload-level:4 -->

These replace ADR-0037 decision 1, except its last sentence, and the
completion-receipt clauses of decisions 2 and 3: that withdrawal never exempts
the completed Spec's PASS receipt, and that completion receipts are checked
before moving. Still in force from ADR-0037: whole-package disposition requires
approval and preserves every member; in an unfinished package, one with a Task
or item that is not terminal, completed and validly cancelled Tasks may remain
and terminal Plans may not; the structured `cancellation` record; that Registry
profile lifecycles decide member terminality while disposition-entry statuses
are registered separately; and that templates do not seed approvals.
ADR-0037 decisions 4 onward, on assessments, history-only availability and
capture identity, are unchanged.

Partially superseded by
[ADR-0051](0051-summarize-and-delete-retirement.md): the archive and
preservation wording in decision 4 ("ready for archive review", "enters the
completed archive", "the preserved copy") no longer applies. A ready package is
deleted once its removal is approved, and its number is reserved.

The `superseded` Spec and Plan status named in decision 1 and decision 4 no
longer exists: SPEC-0256 (retired; version history) removed it from the Stage 01 to 03 lifecycles. The
decision body above is unchanged.

#### Consequences

##### Impacts

Lifecycle generation 6 adds a Registry migration and a Git-bound proof. Active
Tasks were rewritten mechanically; terminal Tasks unchanged since the source
revision keep their generation's reader. A branch still writing generation 5
Evidence must take the same rewrite. REQ-0026-FR-0009 and AD-0030 state the
new waiting rule.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Proposed on 2026-10-13 from the owner's choice of these options. SPEC-0231
implements and verifies it, and SPEC-0233 corrects its reader and text. The
owner accepted this decision on 2026-10-13.

###### Compliance
<!-- core-payload-level:4 -->

SPEC-0231 proves each rule with passing and failing fixtures, loads every
active package under generation 6, and keeps generation 4 and 5 terminal Tasks
byte-identical.

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
