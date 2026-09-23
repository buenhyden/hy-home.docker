---
title: "Lakehouse Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0094"
parent_ids:
- "POL-0094"
implementation_services:
  infra/04-data/lake-and-object/seaweedfs/docker-compose.yml:
  - seaweedfs-table-bucket
  infra/04-data/lakehouse/spark/docker-compose.yml:
  - spark
  infra/04-data/lakehouse/trino/docker-compose.yml:
  - trino
created: "2026-09-23"
---

# Lakehouse Usage Guide

## Usage

### Purpose and classification

The lakehouse is OPTIONAL and selected by `lakehouse`. Tables are Apache
Iceberg in the SeaweedFS `lakehouse` table bucket, catalogued by the SeaweedFS
built-in Iceberg REST catalog. Spark is the batch and table-maintenance
engine and Trino the interactive SQL engine; Flink (S14) joins the same
catalog. Iceberg is a table
format, not a service.

### Current implementation

- **Catalog.** `seaweedfs-s3` serves the REST catalog on
  `http://seaweedfs-s3:${SEAWEEDFS_ICEBERG_PORT:-8181}` on `object_net` only,
  with no route. Requests are SigV4-signed with an S3 identity. The `lakehouse`
  table bucket holds the namespaces `dev` and `test`; `seaweedfs-table-bucket`
  ([SeaweedFS Compose](../../../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml))
  creates the bucket, its policy and the namespaces.
- **Identity.** Every engine uses the `lakehouse` S3 identity (STRG-015). Its
  S3 actions cover only the `lakehouse` bucket, and the table bucket policy
  grants it namespace and table operations but not policy changes or bucket
  deletion. It cannot read other buckets.
- **Spark.** [Spark Compose](../../../../../infra/04-data/lakehouse/spark/docker-compose.yml)
  defines a one-shot job built from `apache/spark` plus the pinned Iceberg Spark
  runtime and AWS bundle. The wrapper writes `spark-defaults.conf` to tmpfs with
  the catalog `lakehouse` as the default catalog and exports the secret into
  the Spark process, so `spark-sql`, `spark-submit` and `pyspark` all see the
  same catalog. Spark runs in local mode with 2 CPUs and 2 GiB, a read-only
  root filesystem and no UI.
- **Trino.** [Trino Compose](../../../../../infra/04-data/lakehouse/trino/docker-compose.yml)
  runs a single-node coordinator (`trinodb/trino`) with the catalog
  `lakehouse`. The catalog file reads the endpoints and the secret from the
  environment (`${ENV:…}`), which the wrapper fills from the Docker secret.
  SigV4 needs the S3 keys set explicitly, and view endpoints are off because
  SeaweedFS serves none. The HTTP API has no authentication, so it is published
  on `127.0.0.1:${TRINO_HOST_PORT:-18090}` only, with no route. It runs with
  2 CPUs, 2 GiB (80% heap), a read-only root and tmpfs for its data directory.

### Commands and side effects

| Command | Effect |
| --- | --- |
| `docker compose --profile lakehouse up spark` | Lists namespaces; writes nothing |
| `docker compose --profile lakehouse run --rm spark /opt/spark/bin/spark-sql -S -e "SHOW TABLES IN dev"` | Read only |
| `… spark-sql -S -e "CREATE TABLE dev.t (…) USING iceberg"` / `INSERT` | Writes table metadata and data files |
| `… -e "CALL lakehouse.system.rewrite_data_files(table => 'dev.t')"` | Compacts data files; adds a snapshot |
| `… -e "CALL lakehouse.system.expire_snapshots(table => 'dev.t', older_than => TIMESTAMP '…')"` | Deletes unreferenced files; time travel before that point is lost |
| `… -e "DROP TABLE dev.t PURGE"` | Deletes the table and its files |
| `docker compose --profile lakehouse up -d trino` | Starts the SQL engine; writes nothing |
| `docker compose exec trino trino --execute "SHOW TABLES FROM lakehouse.dev"` | Read only |
| `… --execute "CREATE TABLE lakehouse.dev.t (…)"` / `INSERT` / `UPDATE` | Writes table metadata and data files |
| `… --execute "ALTER TABLE lakehouse.dev.t EXECUTE optimize"` | Compacts data files; adds a snapshot |
| `… --execute "DROP TABLE lakehouse.dev.t"` | Deletes the table and its files |

## Common Checks

- `HYHOME_COMPOSE_PROFILES=lakehouse bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/check-operations-catalog.py`

## Runbook Handoff

Use the [runbook](runbook.md) for catalog errors, access denied, failed jobs
and table recovery.

## Traceability

- [Policy](policy.md) (`POL-0094`)
- [Runbook](runbook.md) (`RUN-0094`)
- [SeaweedFS guide](../0024-seaweedfs/guide.md)

## Related Documents

- [Spark](../../../../../infra/04-data/lakehouse/spark/README.md) and [Trino](../../../../../infra/04-data/lakehouse/trino/README.md) package READMEs and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [Iceberg Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/)
- [Iceberg REST catalog configuration](https://iceberg.apache.org/docs/latest/spark-configuration/)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)
