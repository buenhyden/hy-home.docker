---
title: "Cancelled Task Acceptance Rule Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0025"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-11-28"
---

# Cancelled Task Acceptance Rule Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion 26/W86 in the [Spec](../spec.md) and [Plan](../plan.md): make
`scripts/lib/document_governance/spec_packages.py` read Criterion Acceptance
the way the [SDLC](../../../00.workspace/03.process/sdlc.md) states it.

##### Inputs and Authority

On 2026-11-28 the user asked in this chat to handle SPEC-0204 criterion 11 by
cancelling TSK-0006 for a successor Task, and, asked here, approved fixing the
validator to match the SDLC. Work ran in the primary checkout from `main`
`7eb128b98`; brief `cancelled-acceptance` bound the changed files. Direct user
authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Changes

| Area | Change |
| --- | --- |
| Defect | The SDLC gives a criterion's one Criterion Acceptance row to a current, non-cancelled Task, but the validator counted a cancelled Task's row too and added its open rows to the unresolved set. A cancelled Task with a frozen legacy row, such as TSK-0006's `11 pending`, therefore blocked any successor from deciding the criterion |
| Fix | `_v6_evidence_contract` reads cancelled Tasks after live ones, skips a cancelled Task's decision row once a live Task holds that criterion, and keeps a cancelled Task's open rows out of the unresolved set. A cancelled row with no live row still stands as history, so existing records such as criterion 12 keep validating |
| Test | `test_a_cancelled_task_neither_decides_nor_blocks_a_criterion`: a live accepted criterion next to a cancelled Task holding a FAIL row and a pending row for it |

##### Blockers and Decisions

The criterion 11 hand-over this fix was for is parked. Cancelling TSK-0006
changes the live work behind criterion 7, whose earlier acceptance in TSK-0005
then fails the current rule because W67 in TSK-0016 has no PASS yet, and the
TSK-0005 table is frozen. The parked hand-over and the 2.7.3 Native log are in
`/home/hyunyoun/p01-evidence/20261128-criterion-11-handover` and need
renumbering before reuse.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 26 | W86 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.document_governance.test_spec_packages -k test_a_cancelled_task_neither_decides_nor_blocks_a_criterion | Test with the fix stashed | FAIL | `criterion 1 has more than one acceptance decision` | required | - |
| E02 | 26 | W86 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.document_governance.test_spec_packages -k test_a_cancelled_task_neither_decides_nor_blocks_a_criterion | With the fix | PASS | OK | required | E01 |
| E03 | 26 | W86 | method=automated; tool=Python3 venv; command=python -m unittest tests.lib.document_governance.test_spec_packages | With the fix | PASS | 168 tests OK in 698 s | required | - |
| E04 | 26 | W86 | method=automated; tool=Python3; command=python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main | Branch | PASS | selected=890 violations=0 | required | - |

##### Resolution Links

E02 resolves E01.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 26 | pending | E01,E02,E03,E04 | Awaiting owner acceptance | @buenhyden |

##### Remaining Conditions

None for criterion 26 beyond owner acceptance.

#### Handoff

##### Promotion Receipt

None needed: the SDLC already states the rule; only the validator changes.

##### Next Owner

@buenhyden decides acceptance of criterion 26.

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
