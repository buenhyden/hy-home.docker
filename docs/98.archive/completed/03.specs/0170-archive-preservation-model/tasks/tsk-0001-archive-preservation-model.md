---
title: Archive Preservation Model Task
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
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

### Closing measurement (2026-09-04, commit ec3012c0)

| Population | Location | Count |
| :--- | :--- | ---: |
| Completed packages | `docs/98.archive/completed/03.specs/` | 21 packages, 23 documents |
| Superseded documents | `docs/98.archive/superseded/` | 4 |
| Retired documents | `docs/98.archive/retired/` | 104 |
| Tombstones | `docs/98.archive/tombstones/` | 104 |
| Terminal documents in Stages 01/02/03/05/90 | — | 0 of 347 |
| Preserved records whose origin path is also live | — | 0 |

Every restored record is byte-identical to the blob at the commit its Tombstone
records, verified for all 104 after writing. The archive is heterogeneous by
design: 49 of the 104 retired records carry `status: active` and 83 carry no
`type`, because that is what they said when they were withdrawn.

Gate results: `run-ci-gate.py --profile full` exits 0 with 17 unittest suites
reporting `OK`. `check-document-corpus-lifecycle.py` reports
`migrations=3 tombstones=104 preserved=131 decisions=250 recovery_rows=338
violations=0`. Document links resolve with zero failures across 672 documents
and 5618 links; metadata contracts report zero violations.

## Review Evidence

Mutation evidence, by claim:

| Claim | Mutation | Result |
| :--- | :--- | :--- |
| The archive path token admits historical filenames | `README`, `01.setup`, three-digit numbers | match; `../` traversal does not |
| Preservation is not retirement | Remove a completed package without `preserved_paths` | `package-retirement-unrecorded` |
| A retirement needs both halves | Delete a preserved record | `tombstone has no preserved record` |
| | Delete a tombstone | `retired record has no tombstone` |
| Completion takes no tombstone | Add one for a `completed` record | `must not carry a tombstone` |
| Active stages hold no terminal document | Mark ADR-0031 `superseded` in place | `remains in an active stage` |
| Preserved links are exempt only as sources | Break a live document's link | still fails |
| | Break a link into the archive | still fails |
| Supersession crosses the archive boundary | Preserve `ADR-0027` | resolves; `ADR-0029` does not dangle |
| ADR coverage survives preservation | Delete the preserved `ADR-0027` | coverage test fails |

Judgment calls recorded rather than assumed:

1. Preserved records are never edited. `type` is not rewritten to satisfy a
   later contract, which is why the three preservation profiles declare
   `frontmatter_policy: unmanaged` and why the exemption is scoped to path
   patterns inside `docs/98.archive/`.
2. `tombstones/` and `retired/` were measured before being kept. `Reason` is
   211 characters at the median and exists in no document; `Replacement` is
   `none` in 73 of 104. The only overlap is `Retired Path`, which is the join
   key between the two records, so the pair is normalization rather than
   duplication. `Recovery Commit` changed role from recovery route to
   verification anchor and the index now says so.
3. `ADR-0030` was superseded rather than amended. A decision log records what
   was decided and when; editing an outcome in place erases that.
4. 76 links whose text disagrees with their target were found during the link
   repointing. All predate this branch and sit in files it never touched, so
   they are reported rather than swept in.

## Commit Ledger

| Commit | Phase |
| :--- | :--- |
| `3c574af8` | Package opened |
| `0e279133` | Phase 1 — register the preservation subtrees, move the superseded set |
| `00d24f99` | Phase 1 — derive the snapshot path from its checker |
| `29a24810` | Phase 1 — include the preserved snapshot in the producer fixture |
| `197f9429` | Phase 2 — preserve the completed packages, separate the two exits |
| `35c02f41` | Phase 2 — source the historical fixture from its preserved copy |
| `58470441` | Phase 2 — align preserved role-link text with its target |
| `0617cca4` | Phase 3 — restore 104 retired documents from their recorded commits |
| `2786478b` | Phase 4 — define what each Stage 98 subfolder owns |
| `e2f515cf` | Phase 4 — supersede ADR-0030 and reconcile its dependents |
| `e6d6e576` | Phase 5 — enforce the decision/body boundary |
| `ec3012c0` | Phase 5 — enforce active-stage occupancy |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
