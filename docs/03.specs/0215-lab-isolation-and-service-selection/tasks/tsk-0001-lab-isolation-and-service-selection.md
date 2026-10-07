---
title: "LAB Isolation and Service Selection Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0215-TSK-0001"
parent_ids:
- "SPEC-0215-PLAN-0001"
created: "2026-10-08"
---

# LAB Isolation and Service Selection Task

## Objective

Keep HA and replica LABs out of the root, make their runs bounded and
self-cleaning, and record why each optional service is or is not resident.

## Inputs and Authorization

The current user request on 2026-10-08 asks to execute prompt 03 of the
analysis pack with per-unit commits and a per-Spec PR merge. It names no HOME
host run or data move, so those lanes stay `NOT_RUN`. Baseline `main`
`a56ab4e5b`. Registry issues SPEC-0215.

## Work Log

### Observed Baseline

The root renders 118 services with `--profile '*'`; none is a LAB service.
Seven LAB files refuse to render without their data, cluster or result roots.
`labs/mongodb.yml` renders without input because its state uses project
named volumes; `labs/opensearch-cluster.yml` does the same for node data.
The root still declares `lab_net` (10.250.9.0/24), which only RedisInsight
joins and which no LAB uses. CouchDB, MongoDB Express and the PostgreSQL
router register `Host(*.${LAB_BASE_DOMAIN})` routers with HOME middleware,
and `LAB_BASE_DOMAIN` equals the HOME domain. Six LABs label their services
`hy-home.tier: data`. No script starts or stops a LAB, and no aggregate HOME
budget exists. `infra/common-optimizations.exceptions.json` names no LAB.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Root closure | 1 | W1 | Root render test RED then GREEN | Pending | NOT_RUN | Pending | pending |
| LAB boundary | 2 | W2 | LAB contract tests and renders | Pending | NOT_RUN | Pending | pending |
| Controller | 3 | W2 | Controller unit and real Docker run | Pending | NOT_RUN | Pending | pending |
| Selection rules | 4 | W3 | Policy and catalog checks | Pending | NOT_RUN | Pending | pending |
| Records | 5 | W4 | Local gate and review | Pending | NOT_RUN | Pending | pending |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
