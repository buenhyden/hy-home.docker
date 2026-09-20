---
title: "Locust Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0062"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Locust Operations Policy

## Overview

Locust is an explicit `testing` capability. It is never part of HOME or broad
tooling startup. The policy protects test targets and prevents unreviewed load,
credential capture, or misleading performance evidence.

## Policy Scope

The `locust-master` and `locust-worker` services, the bind-backed scenario
directory, target authorization, result handling, scaling, and image upgrades.

## Controls

- **Activation:** select only the `testing` profile and name the Locust services.
  Every run records target owner, duration, user/spawn limits, worker count,
  abort SLI, and stop owner. There is no repository-defined generic RPS threshold
  or maintenance window.
- **Authorization:** target credentials use an approved secret channel and may
  not be embedded in `locustfile.py`, Compose, logs, or retained raw results.
- **Data:** scenarios and results remain in the `locust-data` host path. Retain
  sanitized aggregates under the owning Task/incident; do not retain payloads or
  identifiers without an explicit evidence need.
- **Resources:** worker scaling is explicit and bounded by the approved test.
  Stop workers and master after the run; never add restart behavior that replays
  load after a host restart.
- **Backup:** copy the scenario/result directory only while the test is stopped.
  Repository-tracked scenarios are restored from Git; untracked result recovery
  must be rehearsed in a separate directory before overwrite.
- **Upgrade:** review Locust/Python dependency release notes, rebuild from the
  tracked Dockerfile, and run a small approved canary before restoring the
  normal test envelope.
- **Removal:** remove the service only after scenario ownership, retained
  evidence, and all consumers are accounted for. Deleting the host directory is
  a separate destructive action.

## Exceptions

Any deviation must name target, blast radius, expiry, stop condition, and
recovery owner. An exception cannot waive target authorization or secret handling.

## Verification

Static Compose and hardening checks prove configuration only. Runtime evidence
must include worker registration, target SLI, sanitized results, and final stopped
state.

## Review Cadence

Review when profiles, Dockerfile dependencies, scenario storage, target network,
or scaling behavior changes.

## Traceability

- [Guide](guide.md) (`GDE-0062`)
- [Runbook](runbook.md) (`RUN-0062`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

## Related Documents

- [Locust Compose source](../../../../../infra/09-tooling/locust/docker-compose.yml)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [Locust documentation](https://docs.locust.io/en/stable/)
- [Operations index](../../../README.md)
