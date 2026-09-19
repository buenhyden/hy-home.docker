---
title: "SurrealDB Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0080"
parent_ids:
- "POL-0080"
created: "2026-09-19"
---

# SurrealDB Guide

## Usage

OPTIONAL database for Open Notebook; enable when that consumer is required.

Profiles: `surrealdb / notebook / admin`. Services: `surrealdb`. Root Compose owns inclusion.

Dockerfile and entrypoint own the server; internal listener is fixed at 8000. SURREALDB_HOST_PORT changes only the loopback host mapping. surrealdb-data mounts /mydata; surreal_db_password supplies authentication without a literal in Compose.

[Implementation](../../../../../infra/04-data/specialized/surrealdb/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Common Checks

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0004](../../../../02.architecture/descriptions/0004-data-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://surrealdb.com/docs/surrealdb/cli/start)
