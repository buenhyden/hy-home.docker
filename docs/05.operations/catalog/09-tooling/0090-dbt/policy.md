---
title: "dbt Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "POL-0090"
parent_ids:
- "AD-0009"
created: "2026-09-21"
---

# dbt Operations Policy

## Overview

dbt writes derived relations into the application database. Its privileges must
stay limited to reading sources and owning its target schema.

## Policy Scope

Provisioning, grants, commands with side effects, credentials and removal.

## Controls

- Select only through `analytics-engineering`; never make dbt a long-running
  service or add an OIDC web front end for it.
- dbt grants live in the feature provisioning SQL, not in `mng-pg-init`. The role
  is `NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION` and never owns the
  source schema. The target schema must differ from the source schema.
- `run`, `build` and `--full-refresh` require a reviewed model selection.
  `--version` or `debug` output is never recorded as a model run.
- Keep project and profiles read-only; generated artifacts stay on tmpfs.

## Exceptions

None. Widening grants (for example `CREATE` on the database) needs a reviewed
change naming the reason.

## Verification

Static rendering and provisioning tests; the disposable rehearsal proves read
on the source, write on the target and denial on the source schema.

## Review Cadence

Review on dbt or adapter upgrade, new sources, and grant changes.

## Traceability

- [Guide](guide.md) (`GDE-0090`)
- [Runbook](runbook.md) (`RUN-0090`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Image Dockerfile](../../../../../infra/09-tooling/dbt/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [dbt Compose source](../../../../../infra/09-tooling/dbt/docker-compose.yml)
- [Management database policy](../../04-data/0028-management-database/policy.md)
