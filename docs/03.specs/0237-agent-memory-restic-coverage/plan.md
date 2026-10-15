---
title: "Agent Memory Restic Coverage Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0237-PLAN-0001"
parent_ids:
- "SPEC-0237"
created: "2026-10-13"
---

# Agent Memory Restic Coverage Plan

## Overview

Write the failing test, add the step, update the policy row and the
runbook, then review and observe one real run.

## Scope

W1 adds the existing CLI's SQLite backup to daily Restic staging with
synthetic absent-store and failure cases; W2 updates POL-0021 and RUN-0021.
W3 reviews the source, and W4 separately observes a real HOME backup;
Compose, include sets, systemd and retention are unchanged.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Backup step and its harness test | None | TSK-0001 | Task evidence |
| W2 | 2 | POL-0021 row and RUN-0021 procedure | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Independent IaC review | W1, W2 | TSK-0001 | Task evidence |
| W4 | 4 | One real `hyhome-backup.service` run on HOME | W3 | TSK-0001 | Task evidence |

## Verification Plan

Run the new harness test against the `main` script (RED) and the changed
script (GREEN), the backup contract tests, `bash -n` and shellcheck, the
script manifest check, changed metadata, corpus lifecycle, links and
markdownlint. W4 reads the run journal and lists the snapshot for the file
name only.

## Risks and Recovery

### Risks and Rollback

- **Plaintext in staging.** The copy is plaintext like the other exports and
  is removed by the EXIT trap; Restic stores it encrypted.
- **A failing step fails the unit.** A broken store marks the daily run
  failed, which the `HyhomeBackupStale` alert reports.
- **Rollback.** Revert the commits; the manual command in RUN-0021 still
  works.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-agent-memory-restic-coverage.md)
