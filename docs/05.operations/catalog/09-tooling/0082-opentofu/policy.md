---
title: "OpenTofu Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0082"
parent_ids:
- "AD-0009"
created: "2026-09-19"
---

# OpenTofu Policy

## Overview

DEV operator job; excluded from HOME automatic startup.

## Policy Scope

`infra/09-tooling/opentofu` and services `opentofu` under profiles `iac / tooling`.

## Controls

Only explicit run commands are permitted. A plan may contact remote providers and must use an approved account/workspace; apply/destroy are separately reviewed actions. Never publish state or plan contents because they may contain secrets.

[Implementation](../../../../../infra/09-tooling/opentofu/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

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
- [Upstream documentation](https://opentofu.org/docs/cli/commands/plan/)
