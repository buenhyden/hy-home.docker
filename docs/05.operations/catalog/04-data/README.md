# Operations — 04 Data

> Data operations documents grouped by stable analytics, storage, and database subjects.

## Overview

This domain co-locates each existing guide, policy, and runbook under its frozen
`ops-0017` through `ops-0035` identity without adding a role that did not exist
in the migration ledger.

## Audience

- Operators, SREs, data platform engineers, developers, and AI agents.

## Scope

- Existing data service usage, operational controls, recovery procedures, and
  source-only validation boundaries.
- No service startup, data mutation, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [Analytics — InfluxDB](ops-0017-influxdb/guide.md) | [Guide](ops-0017-influxdb/guide.md), [Policy](ops-0017-influxdb/policy.md), [Runbook](ops-0017-influxdb/runbook.md) |
| [Analytics — ksqlDB](ops-0018-ksqldb/guide.md) | [Guide](ops-0018-ksqldb/guide.md), [Policy](ops-0018-ksqldb/policy.md), [Runbook](ops-0018-ksqldb/runbook.md) |
| [Analytics — OpenSearch](ops-0019-opensearch/guide.md) | [Guide](ops-0019-opensearch/guide.md), [Policy](ops-0019-opensearch/policy.md), [Runbook](ops-0019-opensearch/runbook.md) |
| [Analytics — Warehouses](ops-0020-starrocks/guide.md) | [Guide](ops-0020-starrocks/guide.md), [Policy](ops-0020-starrocks/policy.md), [Runbook](ops-0020-starrocks/runbook.md) |
| [Backup policy](ops-0021-backup-and-restore/policy.md) | [Policy](ops-0021-backup-and-restore/policy.md) |
| [Cache and KV — Valkey Cluster](ops-0022-valkey-cluster/guide.md) | [Guide](ops-0022-valkey-cluster/guide.md), [Policy](ops-0022-valkey-cluster/policy.md), [Runbook](ops-0022-valkey-cluster/runbook.md) |
| [Lake and Object — MinIO](ops-0023-minio/guide.md) | [Guide](ops-0023-minio/guide.md), [Policy](ops-0023-minio/policy.md), [Runbook](ops-0023-minio/runbook.md) |
| [Lake and Object — SeaweedFS](ops-0024-seaweedfs/guide.md) | [Guide](ops-0024-seaweedfs/guide.md), [Policy](ops-0024-seaweedfs/policy.md), [Runbook](ops-0024-seaweedfs/runbook.md) |
| [NoSQL — Cassandra](ops-0025-cassandra/guide.md) | [Guide](ops-0025-cassandra/guide.md), [Policy](ops-0025-cassandra/policy.md), [Runbook](ops-0025-cassandra/runbook.md) |
| [NoSQL — CouchDB](ops-0026-couchdb/guide.md) | [Guide](ops-0026-couchdb/guide.md), [Policy](ops-0026-couchdb/policy.md), [Runbook](ops-0026-couchdb/runbook.md) |
| [NoSQL — MongoDB](ops-0027-mongodb/guide.md) | [Guide](ops-0027-mongodb/guide.md), [Policy](ops-0027-mongodb/policy.md), [Runbook](ops-0027-mongodb/runbook.md) |
| [Operational — MNG-DB](ops-0028-management-database/guide.md) | [Guide](ops-0028-management-database/guide.md), [Policy](ops-0028-management-database/policy.md), [Runbook](ops-0028-management-database/runbook.md) |
| [Operational — Supabase](ops-0029-supabase/guide.md) | [Guide](ops-0029-supabase/guide.md), [Policy](ops-0029-supabase/policy.md), [Runbook](ops-0029-supabase/runbook.md) |
| [Optimization hardening](ops-0030-optimization-hardening/guide.md) | [Guide](ops-0030-optimization-hardening/guide.md), [Policy](ops-0030-optimization-hardening/policy.md), [Runbook](ops-0030-optimization-hardening/runbook.md) |
| [Relational — PostgreSQL Cluster](ops-0031-postgresql-cluster/guide.md) | [Guide](ops-0031-postgresql-cluster/guide.md), [Policy](ops-0031-postgresql-cluster/policy.md), [Runbook](ops-0031-postgresql-cluster/runbook.md) |
| [PostgreSQL logical upgrade restore rehearsal](ops-0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) | [Runbook](ops-0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) |
| [Specialized — Neo4j](ops-0033-neo4j/guide.md) | [Guide](ops-0033-neo4j/guide.md), [Policy](ops-0033-neo4j/policy.md), [Runbook](ops-0033-neo4j/runbook.md) |
| [Specialized — Qdrant](ops-0034-qdrant/guide.md) | [Guide](ops-0034-qdrant/guide.md), [Policy](ops-0034-qdrant/policy.md), [Runbook](ops-0034-qdrant/runbook.md) |
| [Storage exhaustion](ops-0035-storage-exhaustion/runbook.md) | [Runbook](ops-0035-storage-exhaustion/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../../README.md)
- [Data infrastructure](../../../../infra/04-data/README.md)
- [Guides index](README.md)
- [Policies index](README.md)
- [Runbooks index](README.md)
- [Incident records](../../incidents/README.md)
