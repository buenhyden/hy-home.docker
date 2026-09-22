---
title: "MLflow Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "POL-0088"
parent_ids:
- "AD-0011"
created: "2026-09-21"
---

# MLflow Operations Policy

## Overview

MLflow is an OPTIONAL tracking service. Its database and artifact store are
feature-owned resources on shared infrastructure and must never widen the
privileges of that infrastructure.

## Policy Scope

Activation, database and artifact provisioning, authentication, credential
handling, backup/restore, upgrade and removal of the MLflow tracking server.

## Controls

- Select only through `mlops` or `data-science`; never add it to HOME or the
  current operating command without an explicit decision.
- MLflow SQL lives in the feature provisioning file. The shared `mng-pg-init`
  job must not read MLflow secrets or run MLflow DDL.
- The MLflow database role is `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
  NOREPLICATION`. Provisioning refuses an administrator role and a database
  owned by another role instead of taking it over.
- The server uses the bucket-scoped SeaweedFS identity only. Do not give MLflow or
  any SDK the SeaweedFS admin credential or another consumer's identity.
- Credentials reach the process through the environment, never argv or the
  backend URI.
- Keep gateway SSO on the route. Adopting the community OIDC plugin or
  `basic-auth` is a separate reviewed change with UI, API and SDK acceptance.
- Back up database and bucket together and verify restore in isolation before
  an upgrade.

## Exceptions

Internal SDK access on `infra_net` is unauthenticated. This is an accepted,
recorded gap until an MLflow-level authentication path is approved; it is not
an assurance. No exception may disable gateway SSO.

## Verification

Static profile rendering, provisioning contract tests and the disposable
PostgreSQL rehearsal. Live verification requires: route returns 401 without a
session, a run with an artifact round-trips through the proxy, the MLflow SeaweedFS
user is denied on another bucket, and a restore rehearsal.

## Review Cadence

Review on MLflow upgrade, authentication change, bucket or database rename,
and credential rotation.

## Traceability

- [Guide](guide.md) (`GDE-0088`)
- [Runbook](runbook.md) (`RUN-0088`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Image Dockerfile](../../../../../infra/11-laboratory/mlflow/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [MLflow Compose source](../../../../../infra/11-laboratory/mlflow/docker-compose.yml)
- [Management database policy](../../04-data/0028-management-database/policy.md)
- [SeaweedFS policy](../../04-data/0024-seaweedfs/policy.md)
