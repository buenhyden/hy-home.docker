---
title: "OpenBao ADR Acceptance Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0038"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# OpenBao ADR Acceptance Task

## Overview

### Objective

Execute W54: accept ADR-0050, mark ADR-0003 and ADR-0018 superseded by it,
and move both to the superseded archive. This Task owns criterion 49 only.

## Inputs and Authorization

On 2026-10-29 the owner approved a new OpenBao ADR that supersedes ADR-0003
and ADR-0018. TSK-0036 added ADR-0050 as `proposed`, because a new ADR must
start there and only an accepted ADR can supersede. The input is `main` at
merged PR #636. The authorization covers the acceptance, the archive move,
this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0038 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0038 | ready | in-progress | #objective |
| SPEC-0212-TSK-0038 | in-progress | completed | #evidence |

### Change

`a03c3748a` accepts ADR-0050 with `supersedes` naming ADR-0003 and ADR-0018,
and marks both `superseded` with `superseded_by: "ADR-0050"` in place.
`25f2d8ef2` moves both unchanged to `docs/98.archive/superseded/`, with
catalog rows whose source is `a03c3748a`. REQ-0003, AD-0003, AD-0018 and
ADR-0042 now cite ADR-0050 instead of linking into the archive.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Changed metadata | 49 | W54 | `check-document-metadata.py --mode check-changed` against `origin/main` | This branch | PASS | 0 violations | required | - |
| Metadata contracts | 49 | W54 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Link check | 49 | W54 | `check-document-links.py --mode all` | This branch | PASS | 0 failures | required | - |
| Corpus and archive | 49 | W54 | `check-document-corpus-lifecycle.py --base-ref origin/main` | This branch | PASS | 0 violations; archive recovery 0 violations with 116 preserved units | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 49 | accepted | Changed metadata, Metadata contracts, Link check, Corpus and archive | ADR-0050 is the accepted secrets manager decision and the Vault ADRs are preserved as superseded. | SPEC-0212 TSK-0038 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Investigation records](tsk-0036-investigation-records-and-currency-fixes.md)
