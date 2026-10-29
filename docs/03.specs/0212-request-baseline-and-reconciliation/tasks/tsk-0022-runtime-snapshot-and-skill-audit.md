---
title: "Runtime Snapshot and Skill Audit Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0022"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Runtime Snapshot and Skill Audit Task

## Overview

### Objective

Execute W38: record a read-only runtime snapshot and audit the canonical
skills for needed references or scripts. This Task owns criterion 33 only.

## Inputs and Authorization

On 2026-10-29 the owner chose to read the state of running containers without
changing any, to audit skill bundles before creating any, and to keep the Codex
loader `NOT_RUN`. The input is `main` at merged PR #619. The authorization
covers `docker ps` and `docker inspect` reads, this branch, its pull request,
and merge. It grants no container start, stop, restart, or recreation.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0022 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0022 | ready | in-progress | #objective |
| SPEC-0212-TSK-0022 | in-progress | completed | #evidence |

### Runtime snapshot

Read on 2026-10-29 with `docker ps`, `docker ps -a`, and `docker inspect`; no
environment variable or secret value was printed.

| Group | Count | State |
| --- | --- | --- |
| `hy-home-infra` running | 60 | 59 healthy; `airflow-statsd-exporter` reports no healthcheck |
| `hy-home-infra` exited | 5 | One-shot provisioning jobs, all `Exited (0)` |
| Other running | 5 | hy-home.k8s `k3d` cluster; outside this repository |

`airflow-statsd-exporter` is drift, not a design gap.
`infra/07-workflow/airflow/docker-compose.yml` declares a `wget` healthcheck
on `/metrics`, last changed 2026-10-28, but the running container was created
on 2026-10-08 and `docker inspect` shows no healthcheck. Recreating that one
container applies it; that is a runtime change for the owner and was not made.

### Skill bundle audit

Of 24 canonical skills, 6 already carry `references/`, `scripts/`, or
`assets/`: `infra-validate`, `policy-gate-agent`,
`provider-model-evaluation`, `security-audit`,
`stateful-recovery-contract-review`, and `style-validation`. Every SKILL.md
link to a bundled file resolves (TSK-0021).

The other 18 are short procedures that route to canonical owners: governance
policies, roles, and the registered scripts in `scripts/manifest.yaml`, whose
selection the quality policy's verification matrix owns. A per-skill copy of
such a script or policy would give one check two owners, which the request
rules out. None of the 18 needs a bundle now; a skill gains one when its
procedure needs domain detail or a deterministic helper that no canonical
owner holds. No skill names a check command in its gates, because the
verification matrix selects checks; this is consistent, not a gap.

Existing skills keep the section layout they were written with; the
subtopics TSK-0015 added to the skill template apply to new skills.

### Codex loader

The Codex loader stays `NOT_RUN` by the owner's choice.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime snapshot | 33 | W38 | `docker ps`, `docker ps -a`, `docker inspect airflow-statsd-exporter` | 2026-10-29 | PASS | 59 of 60 healthy; one recorded drift | required | - |
| Skill inventory | 33 | W38 | Per-skill line, link, and bundle inventory of `.agents/skills/*/` | This branch | PASS | 6 bundled, 18 routing | required | - |
| Metadata contracts | 33 | W38 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Runtime drift correction | 33 | W38 | Recreate `airflow-statsd-exporter` | - | NOT_RUN | Runtime change not authorized | optional | - |
| Codex loader acceptance | 33 | W38 | Native Codex session load | - | NOT_RUN | Owner kept it out of scope | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 33 | accepted | Runtime snapshot, Skill inventory, Metadata contracts | Running state recorded with one drift left for the owner; no skill needs a new bundle; the Codex loader stays not run. | SPEC-0212 TSK-0022 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
