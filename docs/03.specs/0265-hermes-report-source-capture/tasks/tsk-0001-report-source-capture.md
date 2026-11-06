---
title: "Hermes Report Source Capture Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0265-TSK-0001"
parent_ids:
- "SPEC-0265-PLAN-0001"
created: "2026-11-06"
---

# Hermes Report Source Capture Task

## Overview

### Objective

Record the execution and evidence of work units W1 to W9 of the Plan. Nothing
is implemented or run yet.

## Inputs and Authorization

On 2026-11-06 the owner approved drafting this contract ("초안 작성 (권장)")
and chose to exclude the 16 existing reports from backfill ("Backfill 제외
(권장)"). Implementation, Spec approval and every runtime step (Gateway backup,
restore test, cutover, backfill apply, plugin install, restart, cron prompt
update) still need the owner's separate approval.

Inputs, as data: the read-only host and Blog-data findings of 2026-11-06, and
the operator's untracked contract change request of 2026-11-06. Its section 1
(a separate artifact tool) was considered and not chosen, see ADR-0060; its
sections 2 and 3 are scoped decisions in the Spec; its section 4 (the sidecar
failure streak) is an out-of-scope follow-up.

## Work Log

### Open Items

The H, D and G items come from the owner's 2026-11-06 request and are mapped
in criterion 9 (controller answer, not Spec approval). Oversized reports go
`BLOCKED`, never truncated (owner: explicit BLOCKED when the original cannot be
obtained). Still open for the owner:

- Whether a Hermes-specific REQ or AD should parent this package instead of the
  SPEC-0212 parents.
- Who owns Blog-data's per-report backfill exclusion, a prerequisite of W8, and
  when.
- The stale server A state (a43d824334, schema 3) in Blog-data runbook 0008.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2, 4, 6 | W1 | plugin unit tests for the report argument, store, `source_text` and rejections | not yet written | NOT_RUN | - | required | - |
| E2 | 3 | W2 | plugin test for the receipt-set private record and `source_ref` | not yet written | NOT_RUN | - | required | - |
| E3 | 5 | W3 | derivation test: Gateway, email and Telegram share one stored-bytes digest | not yet written | NOT_RUN | - | required | - |
| E4 | 7, 8, 9 | W4 | deploy script and prompt tests; scratch path check | not yet written | NOT_RUN | - | required | - |
| E5 | 10 | W5 | metric label test, rule and dashboard lint | not yet written | NOT_RUN | - | required | - |
| E6 | 11 | W6 | document metadata, links, lifecycle and contract checks on the implementation | not yet run on the implementation | NOT_RUN | - | required | - |
| E7 | 12 | W7 | schema-4 backup, restore test on a copy, cutover | owner approval pending | NOT_RUN | - | required | - |
| E8 | 13 | W8 | `backfill-reports` dry run shows the 16 reports excluded; apply | Blog-data capability and owner approval pending | NOT_RUN | - | required | - |
| E9 | 12, 14 | W9 | plugin install, restart, cron update, one observed run per job; rollback reading | owner approval pending | NOT_RUN | - | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1 | owner acceptance | @buenhyden |
| 2 | pending | E1 | owner acceptance | @buenhyden |
| 3 | pending | E2 | owner acceptance | @buenhyden |
| 4 | pending | E1 | owner acceptance | @buenhyden |
| 5 | pending | E3 | owner acceptance | @buenhyden |
| 6 | pending | E1 | owner acceptance | @buenhyden |
| 7 | pending | E4 | owner acceptance | @buenhyden |
| 8 | pending | E4 | owner acceptance | @buenhyden |
| 9 | pending | E4 | owner acceptance | @buenhyden |
| 10 | pending | E5 | owner acceptance | @buenhyden |
| 11 | pending | E6 | owner acceptance | @buenhyden |
| 12 | pending | E7, E9 | owner acceptance | @buenhyden |
| 13 | pending | E8 | owner acceptance | @buenhyden |
| 14 | pending | E9 | owner acceptance | @buenhyden |

## Review and Completion

Open. The Spec, Plan and this Task are drafts for owner review. Every evidence
row is NOT_RUN: nothing is implemented, and no runtime operation has run.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0060](../../../02.architecture/decisions/0060-hermes-report-source-contract.md)
