---
title: "Agent Memory Restic Coverage Task"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0237-TSK-0001"
parent_ids:
- "SPEC-0237-PLAN-0001"
created: "2026-10-13"
---

# Agent Memory Restic Coverage Task

## Overview

### Objective

Put the shared agent memory store into the daily Restic backup, as SPEC-0237
states.

## Inputs and Authorization

- **Request:** the owner asked on 2026-10-13 to review and proceed with Restic
  coverage for the memory store, which SPEC-0236 had deferred.
- **Baseline:** `main` `f1214c839`.
- **Not done:** no real backup run, restore or HOME change; the real store's
  contents were not read.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0237 | draft | approved | #owner-decision-2026-10-29 |
| SPEC-0237-PLAN-0001 | draft | approved | #owner-decision-2026-10-29 |
| SPEC-0237-TSK-0001 | draft | ready | #inputs-and-authorization |
| SPEC-0237-TSK-0001 | ready | in-progress | #w1-backup-step |
| SPEC-0237-TSK-0001 | in-progress | completed | #owner-decision-2026-10-29 |

### W1 Backup Step

`hyhome-backup.sh` gains one step after `backup-sqlite-export` and before
the SeaweedFS export, so it runs before the Restic backup. If
`$repo_root/.workspace-memory/memory.sqlite3` does not exist, it prints
"agent memory store absent: backup skipped" and moves on, because the CLI
would create an empty store. Otherwise it runs
`python3 "$repo_root/scripts/operations/agent_memory.py" backup --output
"$staging/agent-memory.sqlite3"`; on failure it removes the output and sets
`status=1`. The service runs as `hyunyoun`, and staging is 0700 and owned by
that user, which the CLI requires. The header comment lists the new export.

`BackupContractTests.test_orchestrator_backs_up_the_shared_memory_store_into_staging`
extracts the step and runs it with a stand-in `python3` for three cases:
store absent (exit 0, skip note, CLI not called), present (exit 0, the exact
backup command, output written) and failing (exit 1, output removed). It also
checks that the step comes before `restic backup`. Against the `main` script
it failed (the step is missing); on the change the class ran 13 tests, OK.

### W2 Policy and Runbook

POL-0021 (1.5.6) lists the store as a protected data set: copied by the
script into staging, then Restic, skipped when absent, RPO 24 hours as a
planning target, never restored on HOME. RUN-0021 (1.4.19) states the daily
backup and how to restore from a Restic snapshot through the existing
`restore` command; the manual backup command stays for ad-hoc use. SPEC-0236's
Task points to this package for the coverage it deferred.

### W3 IaC Review

An independent `iac-reviewer` review of `3a8a8f941` returned READY with notes.
It confirmed the step runs after `backup-sqlite-export` and before
`restic backup`, that the EXIT trap removes the file, that a CLI failure inside
the `elif !` condition cannot trigger `set -e`, and that the service user and
the main checkout meet the CLI's directory and repository checks. Notes
applied:

- A dangling symlink at the store path was treated as absent and skipped. The
  check is now `[[ ! -e && ! -L ]]`, so a symlink reaches the CLI, which
  refuses it; a new `dangling` test case failed against the old check and
  passes now. A comment records that `$repo_root` is the main checkout the
  unit runs and that a write held longer than 5 s fails the step.
- RUN-0021 (1.4.20) now names the snapshot path
  `/src/state/exports/agent-memory.sqlite3`, the `hyhome-state` snapshot and
  section 6's scratch restore, and says `restore` runs from the main checkout.

Left as notes: the test stubs `python3`, so the real directory and owner
checks are proven only by the W4 real run, and the README's
`BACKUP_STATE_MAX_GIB` default (8) differs from the compose default (5), which
predates this change.

### W4 Real Run

After #455 merged as `caa8f1b96`, the owner started `hyhome-backup.service` on
2026-10-13; it ended at 22:08:04 KST with `failed`. The journal shows the
memory step wrote `/home/hyunyoun/backups/staging/agent-memory.sqlite3` with no
`agent memory backup failed` line. The run's only failure line is the known
recovery gap, "OpenBao snapshot token absent: snapshot failed". The latest
`hyhome-state` snapshot `ae96be5f` (2026-10-13 13:06:50 UTC) lists
`/src/state/exports/agent-memory.sqlite3`; only paths were listed, not
contents. The offsite copy reported 7 snapshots in R2.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step test | 1 | W1 | Harness test RED on the `main` script, GREEN after; backup contract tests (13) | Branch on `f1214c839` | PASS | W1 Backup Step | required | - |
| Step contract tests | 2 | W1 | Backup contract tests (13) on the new step | Branch on `f1214c839` | PASS | W1 Backup Step | required | - |
| Checks | 2 | W2 | `bash -n` and shellcheck; script manifest; backup contract and tier layout tests (23); changed metadata (7 documents) and corpus lifecycle, 0 violations; links `--mode all` 0 failures; Registry identity tests; markdownlint | `06da0708f` | PASS | W2 Policy and Runbook | required | - |
| IaC review | 3 | W3 | Independent `iac-reviewer`: READY with notes, notes applied | `3a8a8f941` | PASS | W3 IaC Review | required | - |
| Symlink case | 1 | W1 | `dangling` case RED against the old check, GREEN after; shellcheck | Branch | PASS | W3 IaC Review | required | - |
| Real run | 4 | W4 | One `hyhome-backup.service` run includes `agent-memory.sqlite3`; memory step succeeded, run failed only on the known OpenBao token gap | snapshot `ae96be5f` | PASS | W4 Real Run | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Step test, Symlink case | Owner accepted on 2026-10-29 on this PASS row. | SPEC-0237 TSK-0001 |
| 2 | accepted | Checks | Owner accepted on 2026-10-29 on this PASS row. | SPEC-0237 TSK-0001 |
| 3 | accepted | IaC review | Owner accepted on 2026-10-29 on this PASS row. | SPEC-0237 TSK-0001 |
| 4 | accepted | Real run | Owner accepted on 2026-10-29 on this PASS row. | SPEC-0237 TSK-0001 |

## Review and Completion

### Owner decision 2026-10-29

The owner decided to close this package on documents alone and ratified Spec
and Plan approval after the fact. Criteria 1 to 4 are accepted on the PASS
rows named in Criterion Acceptance; criterion 4 rests on the Real run row
(snapshot `ae96be5f`). No runtime was rerun. The OpenBao snapshot-token gap
that failed the whole service run is separate from this package.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
