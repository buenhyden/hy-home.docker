---
title: "DEV Data Boundary and InfluxDB Retirement Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
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

## Verification Plan

Use focused unit tests for the provisioner and the variable boundary, a
non-interference render, an isolated `dev-pg` container on a private network
with synthetic secrets and tmpfs data, and the registered changed-profile
local gate with the pinned staged lint. Remote PR `candidate-quality` owns
candidate acceptance. The isolated containers use their own project name and
are removed after the run; no HOME service is touched.

## Risks and Rollback

Revert the logical commits to restore the InfluxDB source and documents; the
archived bytes return through the same revert. The preserved data directory
is untouched, so no data rollback is needed. Reverting the provisioner leaves
already applied connection limits in place; reset one with
`ALTER ROLE <role> CONNECTION LIMIT -1` if required.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-dev-data-and-influx-retirement.md)
