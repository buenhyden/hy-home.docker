---
title: Archive Preservation Model Task
version: 1.0.0
type: sdlc/task
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0170-TSK-0001
parent_ids: [SPEC-0170, SPEC-0170-PLAN-0001]
created: 2026-09-04
updated: 2026-09-04
---

# Archive Preservation Model Task

## Objective

Execute the five phases of the archive preservation plan and record the
evidence for each.

## Inputs

- 104 Tombstones under `docs/98.archive/tombstones/`, each with a
  `Retired Path` and a `Recovery Commit`.
- 21 completed Stage 03 packages and three `superseded` documents:
  `ADR-0027`, `AUD-0033`, `RES-0080`.
- The declared but unused archive vocabulary in the `migration` profile and in
  `common.archive_source_prefixes`.

## Work Log

### Survey baseline (2026-09-04, commit 4c5db8b8)

| Population | Location | Count |
| :--- | :--- | ---: |
| Completed Stage 03 packages | `docs/03.specs` | 21 packages, 23 documents |
| Superseded documents | Stages 02 and 90 | 3 |
| Retired documents | Git objects only | 104 |
| Tombstones | `docs/98.archive/tombstones` | 104 |
| Retained records | — | 0 |

Spike evidence: moving `ADR-0027` into `docs/98.archive/superseded/` produced
exactly one finding, `supersession-dangling` from `ADR-0029`, because the
artifact index does not read the archive. The moved path classified as
`unsupported`, so the three preservation profiles are the first requirement.

## Verification Evidence

Recorded per phase as the work lands.

## Review Evidence

Recorded per phase as the work lands.

## Commit Ledger

| Commit | Phase |
| :--- | :--- |
| pending | Phase 1 declarations |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
