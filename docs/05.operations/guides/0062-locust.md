---
title: "Locust Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0062"
parent_ids:
- "POL-0062"
implementation_services:
  infra/09-tooling/locust/docker-compose.yml:
  - locust-master
  - locust-worker
created: "2026-05-10"
---

# Locust Usage Guide

## Usage

### Purpose and classification

Locust is a DEV-only distributed load generator. It is retained for Python-based
scenarios that need a coordinating web UI and one or more workers. Both
`locust-master` and `locust-worker` belong only to the `testing` profile; broad
`tooling` selection does not start either service. A test run is an external
effect on the named target and requires target-owner approval, limits, and a
stop condition.

### Implementation and data flow

- Source: [Locust Compose](../../../infra/09-tooling/locust/docker-compose.yml)
  and its sibling Dockerfile. The Dockerfile/build declaration owns the runtime
  source; the derived image projection is navigation, not build authority.
- Root selection: `docker compose --profile testing ...` from the repository
  root. The root project supplies the project default network; do not use the leaf as a
  standalone project.
- Flow: operator/browser -> host port `${LOCUST_HOST_PORT:-18089}` -> master UI;
  worker -> `locust-master` over the project default network; master and worker read the shared
  `locust-data` bind-backed volume at `/mnt/locust`.
- Dependency: the worker waits for the master's HTTP healthcheck. Target services
  are deliberately not Compose dependencies and must already be approved and
  reachable.
- Health: the master probes its UI; the worker checks its process. Health does
  not prove that the target is safe or that a test result is valid.
- Resources: both services inherit `template-infra-med`. Compose declares two
  `locust-worker` replicas. An approved test may override that default with
  `--scale locust-worker=N` while still targeting both Locust services.

The scenario directory can contain target URLs, credentials, payloads, and test
results. Keep credentials in an approved secret channel, exclude them from
scenario files and evidence, and sanitize request/response data before retention.

### Normal use

1. Record the target, test owner, maximum users/spawn rate/duration, abort SLI,
   and worker count.
2. From the repository root run `docker compose --profile testing config --quiet`
   and confirm the selected services with `docker compose --profile testing config --services`.
3. Review the scenario in the host directory behind `locust-data`. Confirm that
   it cannot modify production data unless that exact effect was approved.
4. Under runtime approval, start only `locust-master` and `locust-worker`, then
   use the host-bound UI. Stop the run immediately when the target abort SLI is
   crossed.
5. Preserve configuration commit, scenario digest, sanitized aggregate results,
   and final stopped state. Raw request bodies, cookies, tokens, and personal
   data are not evidence.

### Persistence, backup, and upgrade

Locust has no application database. The bind-backed scenario/result directory is
the only local persistent scope. Back it up as ordinary files only while no test
is writing to it; Git-tracked scenarios remain source authority. Before a Locust
or dependency upgrade, validate the scenario syntax in an isolated run, execute
a small approved canary, then compare worker registration and aggregate metrics.
No backup, restore, or load execution was performed by this documentation task.

## Common Checks

- `docker compose --profile testing config --quiet`
- `docker compose --profile testing config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

Use the [runbook](../runbooks/0062-locust.md) to stop load, diagnose worker loss, recover scenario
files, or perform an approved upgrade canary.

## Traceability

- [Policy](../policies/0062-locust.md) (`POL-0062`)
- [Runbook](../runbooks/0062-locust.md) (`RUN-0062`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

## Related Documents

- [Locust distributed load generation](https://docs.locust.io/en/stable/running-distributed.html)
- [Locust running without the web UI](https://docs.locust.io/en/stable/running-without-web-ui.html)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
