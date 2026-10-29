---
title: "Open Spec Reconciliation Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0039"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Open Spec Reconciliation Task

## Overview

### Objective

Execute W55: record the reconciliation of the draft, blocked and in-progress
Spec Packages, and promote the OpenTofu operations documents that replaced
the retired Terraform triplet. This Task owns criterion 50 only.

## Inputs and Authorization

On 2026-10-29 the owner chose the open Spec reconciliation group of the
partly met request lines. A read-only survey compared 47 open documents in
19 packages with the repository, and the owner decided each package. The
owner also approved promoting the 0082 OpenTofu guide, policy and runbook.
The input is `main` at merged PR #650. Each package changed in its own pull
request, one Spec per pull request.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0039 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0039 | ready | in-progress | #objective |
| SPEC-0212-TSK-0039 | in-progress | completed | #evidence |

### Package decisions

| Package | Decision | Pull request |
| --- | --- | --- |
| SPEC-0246 | TSK-0001 completed; all criteria were already accepted | #638 |
| SPEC-0182 | Criteria 8, 9, 11 and 12 accepted; TSK-0003 stays blocked on W7 PITR and W10 R2 restore | #639 |
| SPEC-0204 | TSK-0017 and TSK-0018 moved to in-progress; TSK-0019 completed | #640 |
| SPEC-0219 | Spec and Plan approved; TSK-0001 in-progress; criterion 2 waits on a remote-device MCP login | #641 |
| SPEC-0226 | Spec and Plan approved; TSK-0001 in-progress | #642 |
| SPEC-0229 | Closed; criterion 3 not-required because SPEC-0243 replaced it | #643 |
| SPEC-0228 | Closed on the applied budget, the 2026-10-13 snapshot and the PR #404 run | #644 |
| SPEC-0216 | Closed; criterion 4 on the recorded post-unseal run | #645 |
| SPEC-0213 | Closed; criterion 8 on the owner-run HOME preflight of 2026-10-29 | #646 |
| SPEC-0204 | Criterion 19 split: the proven manual scope accepted, new criterion 22 holds scheduled, concurrent, retry and dead-letter and rotation evidence | #647 |
| SPEC-0214 | TSK-0003 completed | #648 |
| SPEC-0237 | Closed on the real backup run | #649 |
| SPEC-0236 | Closed; the local gate and restic rows optional, owned elsewhere | #650 |
| SPEC-0226 | Criterion 1 accepted: the owner accepted the image scan risk; image upgrades are follow-up | separate pull request |

The owner left SPEC-0204 TSK-0007 as it is. Every package that stays open
needs runtime or owner action this Task cannot take: SPEC-0204 P02 to P10,
SEC01, TSK-0007 and criterion 22; SPEC-0218 P07; SPEC-0244; SPEC-0245;
SPEC-0182 W7 and W10; SPEC-0219 criterion 2; SPEC-0226 criterion 3.

### OpenTofu promotion

GDE-0082, POL-0082 and RUN-0082 move from `draft` to `active`. TSK-0036
retired the Terraform triplet after moving its live migration steps into
these three documents, so they are the current IaC operations owner.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Package pull requests | 50 | W55 | Hosted `candidate-quality` and merge of each package pull request | PR #638 to #650 | PASS | Package decisions | required | - |
| Metadata contracts | 50 | W55 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Changed metadata | 50 | W55 | `check-document-metadata.py --mode check-changed` against `origin/main` | This branch | PASS | 0 violations | required | - |
| Link check | 50 | W55 | `check-document-links.py --mode all` | This branch | PASS | 0 failures | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 50 | accepted | Package pull requests, Metadata contracts, Changed metadata, Link check | Every open package has an owner decision recorded in its own Task, and the OpenTofu documents are the active IaC owner. | SPEC-0212 TSK-0039 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Investigation records](tsk-0036-investigation-records-and-currency-fixes.md)
