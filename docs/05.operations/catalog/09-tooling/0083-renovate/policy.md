---
title: "Renovate Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0083"
parent_ids:
- "AD-0009"
created: "2026-09-19"
---

# Renovate Policy

## Overview

DEV maintenance job; excluded from normal HOME and broad startup.

## Policy Scope

`infra/09-tooling/renovate` and services `renovate` under profiles `dependency-update`.

## Controls

Infra automerge is disabled. Keep regular version updates under the configured soak and groups; security fixes bypass that delay and receive separate review. Dependabot owns Storybook npm, Renovate owns its enabled infrastructure managers. Never run a live update job as a config check.

[Implementation](../../../../../infra/09-tooling/renovate/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Exceptions

Owner @buenhyden must record scope, risk, expiry and exit condition before any deviation. Static configuration is not evidence of live backup or recovery.

## Verification

Compose/profile validation and the [runbook](runbook.md) provide separate static and runtime evidence. Stop on unexpected service, mount, authentication or readiness state.

## Review Cadence

Review monthly and before image, persistence, authentication or exposure changes.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://docs.renovatebot.com/self-hosted-configuration/#allowedcommands)
