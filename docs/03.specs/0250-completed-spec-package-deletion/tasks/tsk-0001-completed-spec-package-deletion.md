---
title: "Completed Spec Package Deletion Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0250-TSK-0001"
parent_ids:
- "SPEC-0250-PLAN-0001"
created: "2026-11-03"
---

# Completed Spec Package Deletion Task

## Overview

### Objective

Implement W1–W5: delete the fully terminal Spec packages, reserve their
numbers, unlink current documents, and keep the checks passing without editing
a terminal Task body.

## Inputs and Authorization

The user directed that completed Spec, Plan, and Task documents in
`docs/03.specs/` be deleted, and chose to keep every package with a
non-terminal Task together with its completed Tasks. The coordinator moved the
branch-integration receipt handoff, Stage 98 preservation readers, and the
REQ-0026, AD-0030, and ADR-0037 revisions to the PR #723 review fix and limited
this Task's governance edits to the package-deletion rule. No push, pull
request, or merge from this Task.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units, and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0250 | draft | approved | #current-contract-decision |
| SPEC-0250-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0250-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0250-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Deleted packages

SPEC-0182, 0207, 0210, 0211, 0213–0217, 0219–0225, 0227–0230, 0232, 0233,
0235–0237, 0239, 0241–0243, 0246 and 0247: 31 packages whose Spec, Plan, and
every Task were terminal. Their numbers joined the Spec `reserved_history`.

### Kept packages

| Package | Reason |
| --- | --- |
| SPEC-0204, 0212, 0218, 0226, 0244, 0245, 0248, 0249 | at least one non-terminal Task |
| SPEC-0208, 0209 | carry the generation 5 Contract Migration proof that admits current terminal Tasks closed under generations 3 and 4 |
| SPEC-0231 | carries the generation 6 Contract Migration proof |

Deleting a proof carrier made `load_spec_packages` fail with "lifecycle
generation migration requires one proof". Moving those proofs out of Stage 03
is an open issue.

### Check changes

- `spec_packages.py`: the SPEC-0211-TSK-0002 Resolves correction and its
  helper are removed, so a terminal Task body admits no change at all.
- `spec_packages.py`: generation 7 historical admission now reads only the
  packages still in the tree. Before, it re-read every package of the
  generation 7 source revision, and a deleted pre-generation-5 Task without an
  `## Evidence` section broke the load. Admission only ever applied to present
  Tasks, so this admits nothing new.
- `links.py`: alignment excuses a missing target only for a link from a
  terminal Task, at a registered Task path, by frontmatter or row-derived
  status, into `docs/03.specs/NNNN-*` where the checked root's Registry reserves
  NNNN. A missing or invalid Registry excuses nothing. This covers 13 links in
  the completed SPEC-0212 Tasks 0003, 0007, and 0009.

### Reference cleanup

- 21 Markdown links in 11 current Stage 02 and Stage 05 documents and 7 links
  in editable Stage 03 documents became plain text.
- RUN-0098 no longer names SPEC-0182 in `parent_ids`; runbook parents are
  optional and no current policy owns the procedure.
- Two README path mentions of SPEC-0220 became the bare ID.
- Prose and code comments naming a deleted ID for lineage stay, as the
  documentation protocol allows. DATA-0096 `data.yaml` is a dated snapshot and
  stays. The CI gate evidence `owner` label `SPEC-0211-TSK-0003` stays; changing
  it is a gate-contract change.

### Test changes

| Test | Change | Reason |
| --- | --- | --- |
| `TerminalTaskResolvesCorrectionTests.test_registered_resolves_correction_matches` | replaced by `TerminalTaskBodyTests.test_the_former_resolves_correction_is_rejected` | the correction was removed; the test now asserts rejection |
| `TerminalTaskResolvesCorrectionTests` path and ID | repointed to a synthetic `0001-example` Task | SPEC-0211 is deleted |
| `RetiredPackageLinkTests` | added | a terminal Task link into a reserved package is excused; editable Task, unreserved number, missing Registry, and self-declared Task cases still fail. A run with the exemption disabled failed (RED) |
| `test_reference` evidence fixture anchor | SPEC-0209 row replaced by the SPEC-0204 row | the anchor must stay in the index |
| `test_ci_gate_plan` | four 0211 path strings repointed to `0001-example` | selector-only paths |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W2 | corpus-lifecycle | tree with the 31 packages deleted | PASS | document corpus lifecycle zero violations; active stage occupancy zero | required | - |
| E2 | 3 | W3 | document-links | alignment mode after the reference cleanup | PASS | 850 documents, 7904 links, zero failures and warnings | required | - |
| E3 | 2 | W3 | metadata-changed | `check-changed --base-ref origin/chore/delete-stage98-archive` before this package | PASS | selected 124, zero violations | required | - |
| E4 | 3 | W1 | link-exemption-tests | `RetiredPackageLinkTests` | PASS | 2 tests OK; failed with the exemption disabled | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. Independent review and hosted CI have not run,
and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
