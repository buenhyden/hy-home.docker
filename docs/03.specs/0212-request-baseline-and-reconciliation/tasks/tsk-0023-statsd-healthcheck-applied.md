---
title: "StatsD Healthcheck Applied Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0023"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# StatsD Healthcheck Applied Task

## Overview

### Objective

Execute W39: record the owner's correction of the runtime drift TSK-0022
found. This Task owns criterion 34 only.

## Inputs and Authorization

TSK-0022 recorded that `airflow-statsd-exporter` ran without the healthcheck
its Compose file declares. On 2026-10-29 the owner chose to recreate it
personally. The agent only read container state with `docker inspect` and
`docker ps`. The input is `main` at merged PR #620.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0023 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0023 | ready | in-progress | #objective |
| SPEC-0212-TSK-0023 | in-progress | completed | #evidence |

### Observations

All times are UTC on 2026-10-29.

| Time | Observation |
| --- | --- |
| 02:48:41 | The owner's recreation created a new container. It carried the declared `wget` healthcheck but stayed in state `created` and did not run. |
| 02:50:41 | The container started; health `starting`. |
| 02:50:48 | The first healthcheck exited 0; health `healthy`, failing streak 0. |

`docker compose --profile workflow-airflow config` renders the same
healthcheck, so the declared and running configuration now agree. After the
start, all 60 running `hy-home-infra` containers report healthy. Airflow's
StatsD metrics had a gap while the container was not running, about two
minutes.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Exporter health | 34 | W39 | `docker inspect airflow-statsd-exporter` health state | 2026-10-29 | PASS | `healthy`, last exit 0 | required | - |
| Declared healthcheck | 34 | W39 | `docker compose --profile workflow-airflow config`, healthcheck field only | `main`@`8a01dd7e6` | PASS | Matches the running container | required | - |
| Project health | 34 | W39 | `docker ps` for project `hy-home-infra` | 2026-10-29 | PASS | 60 of 60 healthy | required | - |
| Metadata contracts | 34 | W39 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 34 | accepted | Exporter health, Declared healthcheck, Project health, Metadata contracts | The exporter runs its declared healthcheck and is healthy; the TSK-0022 drift is closed by the owner's action. | SPEC-0212 TSK-0023 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
