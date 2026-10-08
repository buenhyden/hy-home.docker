---
title: "DEV Data Boundary and InfluxDB Retirement Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0213-PLAN-0001"
parent_ids:
- "SPEC-0213"
created: "2026-10-07"
---

# DEV Data Boundary and InfluxDB Retirement Plan

## Overview

Land the decision and contract first, then the DEV variable and provisioner
change, then the InfluxDB retirement, then the backup evidence. Each work unit
is one reviewable commit.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Accept ADR-0047 and amend the documents it changes | None | TSK-0001 | Task evidence |
| W2 | 2, 3 | Fix DEV consumer variables and add provisioner connection budgets | W1 | TSK-0001 | Task evidence |
| W3 | 4, 5 | Remove InfluxDB source, consumers, tests and operations documents | W1 | TSK-0001 | Task evidence |
| W4 | 6 | Record the DEV backup chain and run the isolated restore canary | W2 | TSK-0001 | Task evidence |
| W5 | 7 | Give DEV exporters monitor accounts and scrape jobs | W2 | TSK-0002 | Task evidence |
| W6 | 8 | Reject empty, shared and nested named-volume paths | None | TSK-0002 | Task evidence |
| W7 | 9 | Enable the DEV WAL archive with retention and rehearse PITR | W4 | TSK-0002 | Task evidence |
| W8 | 10 | Activate the HOME stanza, WAL, first full backup and restore canary | W7 | TSK-0002 | Task evidence |

## Verification Plan

Use focused unit tests for the provisioner and the variable boundary, a
non-interference render, an isolated `dev-pg` container on a private network
with synthetic secrets and dedicated named volumes, and the registered changed-profile
local gate with the pinned staged lint. Remote PR `candidate-quality` owns
candidate acceptance. The isolated containers use their own project name and
are removed after the run (the Task records that removal was denied and
left to the operator); no HOME service is touched.

The 2026-10-08 extension (W5–W8) adds isolated exporter, WAL and PITR runs
with labelled resources and a Compose validation regression. W8 runs on HOME
only after W5–W7 merge, in the order RUN-0021 sets.

## Risks and Rollback

Revert the logical commits to restore the InfluxDB source and documents; the
archived bytes return through the same revert. The preserved data directory
is untouched, so no data rollback is needed. Reverting the provisioner leaves
already applied connection limits in place; reset one with
`ALTER ROLE <role> CONNECTION LIMIT -1` if required. W7 rollback sets
`archive_mode=off` and returns to the earlier image tag; archived WAL and
backups stay in the repository until retention expires them.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-dev-data-and-influx-retirement.md)
- [Task 0002](tasks/tsk-0002-dev-backup-activation-and-monitoring.md)
