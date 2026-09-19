---
title: "SurrealDB Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0080"
parent_ids:
- "AD-0004"
created: "2026-09-19"
---

# SurrealDB Policy

## Overview

OPTIONAL database for Open Notebook; enable when that consumer is required.

## Policy Scope

`infra/04-data/specialized/surrealdb` and services `surrealdb` under profiles `surrealdb / notebook / admin`.

## Controls

Restrict host access to loopback and application access to infra_net. Preserve database namespace and schema alongside data backups. Never change password files to repair a readiness failure.

[Implementation](../../../../../infra/04-data/specialized/surrealdb/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Exceptions

Owner @buenhyden must record scope, risk, expiry and exit condition before any deviation. Static configuration is not evidence of live backup or recovery.

## Verification

Compose/profile validation and the [runbook](runbook.md) provide separate static and runtime evidence. Stop on unexpected service, mount, authentication or readiness state.

## Review Cadence

Review monthly and before image, persistence, authentication or exposure changes.

## Traceability

- Governing architecture: [AD-0004](../../../../02.architecture/descriptions/0004-data-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://surrealdb.com/docs/surrealdb/cli/start)
