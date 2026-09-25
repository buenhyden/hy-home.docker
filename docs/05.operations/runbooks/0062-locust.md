---
title: "Locust Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0062"
parent_ids:
- "GDE-0062"
created: "2026-05-17"
---

# Locust Recovery Runbook

## When to Use

Use when target health degrades during a test, workers disconnect, the master UI
fails, scenario files are damaged, or a Locust image/dependency upgrade needs an
approved canary. All commands run from the repository root.

## Procedure

1. Record target, users, spawn rate, duration, worker count, scenario digest, and
   the first failing target SLI. Do not collect cookies, tokens, or response bodies.
2. Stop load before diagnosis:

   ```bash
   docker compose --profile testing stop locust-worker locust-master
   ```

3. Capture bounded status and logs:

   ```bash
   docker compose --profile testing ps locust-master locust-worker
   docker compose --profile testing logs --tail=200 locust-master locust-worker
   ```

4. Confirm `docker compose --profile testing config --quiet`. Inspect the master
   health failure before recreating a worker. If the target SLI has not recovered,
   leave Locust stopped and escalate to the target owner.
5. When the master is healthy and restart is approved, start the master first,
   then the worker:

   ```bash
   docker compose --profile testing up -d locust-master
   docker compose --profile testing up -d locust-worker
   ```

6. For scenario recovery, keep both services stopped, copy the current
   bind-backed scenario directory to a protected quarantine path, restore the
   reviewed files into a separate directory, compare hashes, and only then
   replace the active files. Never restore captured credentials or raw personal data.
7. For an upgrade, rebuild from the reviewed Dockerfile, start one master and one
   worker, and run a small separately approved canary. Roll back the image/build
   change if workers fail to register or statistics diverge. Keep the target
   stopped between attempts.

### Verification Steps

- Master UI health succeeds and the expected worker count registers.
- A separately approved canary stays within the named target SLI.
- The final full run is either explicitly approved or Locust remains stopped.
- Scenario/result restore and upgrade rehearsal remain **unexecuted** until a
  Task records the protected paths, commands, and observed results.

## Evidence

Record command exits, timestamps, configuration commit, scenario digest, worker
count, sanitized aggregates, target SLI, and final stopped/running disposition.

## Rollback or Recovery

Stop Locust, restore the prior reviewed scenario/build in isolation, then repeat
static validation and a small approved canary. No action in this runbook rolls
back the target service or repairs target data.

## Escalation

Escalate when target health does not recover after load stops, workers cannot
register against a healthy master, scenario provenance is unknown, or secrets or
personal data appear in logs/results.

## Traceability

- [Guide](../guides/0062-locust.md) (`GDE-0062`)
- [Policy](../policies/0062-locust.md) (`POL-0062`)
- [Locust Compose](../../../infra/09-tooling/locust/docker-compose.yml)

## Related Documents

- [Locust Compose source](../../../infra/09-tooling/locust/docker-compose.yml)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Locust distributed mode](https://docs.locust.io/en/stable/running-distributed.html)
- [Operations index](../README.md)
