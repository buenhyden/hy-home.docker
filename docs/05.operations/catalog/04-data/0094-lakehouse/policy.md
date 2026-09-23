---
title: "Lakehouse Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0094"
parent_ids:
- "AD-0004"
created: "2026-09-23"
---

# Lakehouse Operations Policy

## Overview

Iceberg tables live in one SeaweedFS table bucket behind the built-in REST
catalog. Access scope, destructive maintenance and the separation of test data
are the controls.

## Policy Scope

Catalog exposure, engine identities, namespaces, table maintenance, images and
removal.

## Controls

- Select only through `lakehouse`; never add it to HOME.
- The catalog stays on `object_net` with no route and no host port. Engines
  sign with the `lakehouse` identity, whose S3 actions and table bucket policy
  cover only the lakehouse bucket; the policy lists ten namespace and table
  actions and excludes policy changes and bucket deletion. A new engine reuses that identity or gets its
  own scoped one; none uses the admin identity.
- `dev` and `test` hold development and test tables. Production-like data needs
  a separately approved namespace.
- Trino's HTTP API has no authentication: loopback host port only, no route,
  until a reviewed change adds TLS and an authenticator. Its default start
  writes nothing.
- The default Spark command reads only. `expire_snapshots`,
  `remove_orphan_files` and `DROP … PURGE` delete files and need a named table
  and a recorded reason. The same holds for Trino `DROP TABLE` and its
  `expire_snapshots`/`remove_orphan_files` table procedures.
- Engine images pin the base image and the Iceberg jars by checksum; the
  Iceberg version moves in all engines together.

## Exceptions

None. Enabling catalog credential vending or a route needs a reviewed change.

## Verification

Compose rendering, the catalog check, and an isolated run proving the scoped
identity can create, write, compact and drop a table and cannot read another
bucket.

## Review Cadence

Review on a SeaweedFS, Iceberg or engine upgrade, on a new engine, and on any
new namespace.

## Traceability

- [Guide](guide.md) (`GDE-0094`)
- [Runbook](runbook.md) (`RUN-0094`)
- [SeaweedFS policy](../0024-seaweedfs/policy.md)

## Related Documents

- [Spark Compose source](../../../../../infra/04-data/lakehouse/spark/docker-compose.yml)
- [Trino Compose source](../../../../../infra/04-data/lakehouse/trino/docker-compose.yml)
- [Compose profile vocabulary](../../00-workspace/0078-compose-profile-vocabulary/policy.md)
