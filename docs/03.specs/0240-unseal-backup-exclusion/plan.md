---
title: "Unseal Share File Out of Host Backups Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0240-PLAN-0001"
parent_ids:
- "SPEC-0240"
created: "2026-10-14"
---

# Unseal Share File Out of Host Backups Plan

## Overview

Deliver in two pull requests. The first carries the policy, decision and
runbook text and this package, so the owner attests step 5 against the
revised procedure on `main`. The second carries the exclusion, its test and
the restore wording, and merges only after that attestation; then one daily
run is observed.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Host exclusion, its test and a synthetic dry run (separate PR) | None | TSK-0001 | Task evidence |
| W2 | 2 | POL-0085, ADR-0042 and RUN-0085 text | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Independent IaC, security and rules reviews | W1, W2 | TSK-0001 | Task evidence |
| W4 | 4 | Merge after step 5 is attested; observe the next host snapshot | W3 | TSK-0001 | Task evidence |

## Verification Plan

Run the compose baseline tests with the new test, a `--dry-run` of the
pinned `restic/restic` image with the tracked exclude file against a
synthetic tree, markdownlint, changed metadata, corpus lifecycle and links.
W4 lists the next host snapshot for the file name only.

## Risks and Rollback

- **Early merge.** Merged before step 5, new recovery points would hold no
  share while no off-host copy exists. Contract 2 forbids it.
- **Old snapshots.** Existing host and R2 snapshots keep the old shares until
  the owner deletes them; R2's bucket lock is 30 days and 12 months is only
  the `forget-prune` keep policy. A rekey does not change the keys a
  pre-rekey Raft snapshot opens with, so the exposure ends only when the
  pre-exclusion host snapshots are deleted, a separately approved operation.
- **Rollback.** Revert the exclusion line; the next backup copies the file
  again.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-unseal-backup-exclusion.md)
