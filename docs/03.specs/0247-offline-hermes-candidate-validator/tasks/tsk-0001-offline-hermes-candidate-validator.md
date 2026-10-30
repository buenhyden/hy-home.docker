---
title: "Offline Hermes Candidate Validator Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0247-TSK-0001"
parent_ids:
- "SPEC-0247-PLAN-0001"
created: "2026-10-30"
---

# Offline Hermes Candidate Validator Task

## Overview

### Objective

Implement W1–W3 and record each observable criterion separately.

## Inputs and Authorization

The user authorized offline-only validator code, synthetic tests, Stage 03
package and registry/README, Script Manifest, and local logical commits.
Explicit exclusions: Docker service, server transfer, Blog-data writes,
Cron/email changes, credentials or private live input. The user separately
authorized the requested branch, pull request, and conditional merge.

## Work Log

The original PR #677 supplied the reference implementation. Its local staged
document changes were inspected without modifying that worktree. The validator
uses synthetic fixtures; observations below are specific to this new worktree.

### Current contract decision

The user's request authorizes this repository-local offline validator and the
associated Spec, Plan, Task, and checks. The Spec and Plan are approved now for
that scope; this decision does not approve publication, adoption by Blog-data,
or any excluded operation. Earlier work was an isolated draft trial and is not
represented as having run under an earlier approved status.

### Current readiness and execution

The scoped inputs, work units and synthetic checks are recorded in this Task.
The Task is ready and now in progress under the approved parents. Existing
trial results are observations, not final acceptance. Remaining checks, review,
and criterion decisions are pending; this transition does not assert completion.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0247 | draft | approved | #current-contract-decision |
| SPEC-0247-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0247-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0247-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2 | W1 | focused-tests | synthetic v1 fixtures | PASS | 33 passed | required | - |
| E2 | 4 | W3 | script-manifest | worktree before new paths were staged | FAIL | path-untracked and tests-untracked | required | - |
| E3 | 4 | W3 | document-links | entrypoint and navigation modes | PASS | both modes reported zero failures | required | - |
| E4 | 4 | W3 | metadata-active | worktree before new paths were staged | PASS | 495 selected, zero violations; inclusion of new draft documents not confirmed | optional | - |
| E5 | 4 | W3 | script-manifest | after new paths were staged; implementation subsequently modified in worktree | PASS | script manifest is valid | required | E2 |
| E6 | 1, 2 | W1 | regression-red | synthetic producer shape, idea path and output tests before fixes | FAIL | 12 failed, 30 passed; pytest also collected unittest wrappers | optional | - |
| E7 | 2 | W2 | traversal-red | synthetic directory replacement and invalid Cron date/time before fixes | FAIL | 6 failed, 42 deselected; pytest also collected unittest wrappers | optional | - |
| E8 | 1, 2 | W1 | focused-tests | synthetic fixtures after fixes and formatting | PASS | 48 passed; pytest also collected unittest wrappers | required | - |
| E9 | 4 | W3 | lint | validator and synthetic test; ruff check --no-cache | PASS | all checks passed | required | - |
| E10 | 2, 3 | W2 | staged-and-infra-tests | synthetic fixtures after fixes and formatting | PASS | 48 passed; same run as E8 | required | - |
| E11 | 4 | W3 | metadata-changed | new branch before this evidence correction | FAIL | 146 violations: one criterion/work-unit mismatch and 145 Stage 98 type mismatches | required | - |
| E12 | 4 | W3 | metadata-changed | rerun against base 4d540c870 before remote main changed | PASS | selected 4, zero violations | required | E11 |
| E13 | 4 | W3 | metadata-changed | final staged inputs against base e0d68d7ec | PASS | selected 4, zero violations | required | - |
| E14 | 4 | W3 | metadata-active | implementation against base e0d68d7ec | PASS | selected 495, zero violations; complete identity coverage not established | optional | - |
| E15 | 4 | W3 | document-links | entrypoint and navigation after lifecycle anchors | PASS | both modes reported zero failures | required | - |
| E16 | 4 | W3 | corpus-lifecycle | latest base e0d68d7ec, corpus and archive recovery | PASS | zero violations; 5 migrations, 140 tombstones, 116 preserved, 286 decisions, 374 recovery rows | required | - |
| E17 | 4 | W3 | script-manifest | final implementation against base e0d68d7ec | PASS | script manifest is valid | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E8 | - | @buenhyden |
| 2 | accepted | E8, E10 | - | @buenhyden |
| 3 | accepted | E10 | - | @buenhyden |
| 4 | accepted | E9, E13, E14, E15, E16, E17 | - | @buenhyden |

## Review and Completion

Independent validator re-review reported no further material issue in the
reviewed paths after the directory traversal, Cron timestamp, and producer
shape fixes. Its independent standard-library test run passed 32 tests; its
system Python did not have pytest. The reviewer limited the producer comparison
to the inspected contract. A candidate alone cannot prove execution DB mapping,
email delivery, or publication approval.

Independent lifecycle review confirmed that registered event chains can support
the current states without an earlier draft commit. It found no inconsistency
in the observed record and did not directly observe the entire earlier draft
trial. The active metadata check above does not establish whether the new
draft package was included. E13 applies to the staged inputs observed at that
time; subsequent changes need their applicable checks rerun. Corpus lifecycle
and recovery passed in E16, and criterion 4 is accepted for the observed local
checks. Task completion, the exact diff and local commits remain pending.
Remote CI and remote review have not yet run.
No deployment, Blog-data write, or delivery is claimed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
