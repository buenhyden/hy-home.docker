---
title: "Backup Valkey Export Timeout Specification"
version: "0.5.0"
type: "sdlc/spec"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0191"
parent_ids:
- "REQ-0027"
created: "2026-09-29"
---

# Backup Valkey Export Timeout Specification

## Overview

`hyhome-backup.service` failed with result `timeout` on every run from
2026-09-26 to 2026-09-29. Each run finished pgBackRest, then waited in the
`mng-valkey` RDB export (`valkey-cli --rdb -`) until the unit's 4 h limit, so
Restic never ran and no snapshot exists after 2026-09-25. The export normally
takes about 5 s. When systemd ends the run, it kills the `docker exec`
client, but the export process inside the container can outlive it.

What stalled the first export is not established: the container was recreated
on 2026-09-29 and its earlier log is gone, and the export has succeeded since.
This package bounds the step so one stalled export cannot stop the whole run.

## Boundaries and Inputs

In scope: the `mng-valkey` export step of
`infra/09-tooling/restic/bin/hyhome-backup.sh`, its contract test, and
RUN-0021 step 4.

Out of scope: the other export steps, the systemd unit, failure alerting, and
the root cause of the first stall.

## Behavior Contract

1. The export runs with a 300 s limit inside the container, so the export
   process ends in the container when the limit is reached.
2. On failure or timeout the run logs one line, deletes the partial RDB file,
   continues with the remaining steps and Restic, and exits 1.

## Technical Approach

Wrap `valkey-cli --rdb -` in the image's `timeout` inside `docker exec`, and
replace `|| status=1` with a block that logs, deletes the file and sets the
status.

## Interfaces and Data

The output file `staging/mng-valkey.rdb` is unchanged on success. No
environment, Compose or unit change.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| A partial RDB file is backed up as if complete | The file is deleted on any nonzero exit |
| The limit cuts a healthy export short | Exports take about 5 s for 1 to 3 MB; 300 s leaves a wide margin |

## Acceptance Contract

1. The contract test asserts the in-container limit and the partial-file
   deletion, fails before the change and passes after it.
2. The image's `timeout` ends a command with a nonzero status, and the
   export succeeds within the limit on the live `mng-valkey`.
3. RUN-0021 step 4 states the behavior.
4. `run-ci-gate.py --profile full`, `tests/lib` and `tests/validation` pass.

## Traceability

- REQ-0027: the HOME development host.
- RUN-0021 and POL-0021: backup and restore.
- SPEC-0182 Task 0002: the failure record.

## Open Questions

None.

## Operational Impact

Takes effect on the next run of `hyhome-backup.service`; the script is read
from the checkout.
