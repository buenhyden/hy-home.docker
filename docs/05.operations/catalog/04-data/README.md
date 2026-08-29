---
profile_id: operations-domain-readme
---

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
| [Analytics — InfluxDB](0017-influxdb/guide.md) | [Guide](0017-influxdb/guide.md), [Policy](0017-influxdb/policy.md), [Runbook](0017-influxdb/runbook.md) |
| [Analytics — ksqlDB](0018-ksqldb/guide.md) | [Guide](0018-ksqldb/guide.md), [Policy](0018-ksqldb/policy.md), [Runbook](0018-ksqldb/runbook.md) |
| [Analytics — OpenSearch](0019-opensearch/guide.md) | [Guide](0019-opensearch/guide.md), [Policy](0019-opensearch/policy.md), [Runbook](0019-opensearch/runbook.md) |
| [Analytics — Warehouses](0020-starrocks/guide.md) | [Guide](0020-starrocks/guide.md), [Policy](0020-starrocks/policy.md), [Runbook](0020-starrocks/runbook.md) |
| [Backup policy](0021-backup-and-restore/policy.md) | [Policy](0021-backup-and-restore/policy.md) |
| [Cache and KV — Valkey Cluster](0022-valkey-cluster/guide.md) | [Guide](0022-valkey-cluster/guide.md), [Policy](0022-valkey-cluster/policy.md), [Runbook](0022-valkey-cluster/runbook.md) |
| [Lake and Object — MinIO](0023-minio/guide.md) | [Guide](0023-minio/guide.md), [Policy](0023-minio/policy.md), [Runbook](0023-minio/runbook.md) |
| [Lake and Object — SeaweedFS](0024-seaweedfs/guide.md) | [Guide](0024-seaweedfs/guide.md), [Policy](0024-seaweedfs/policy.md), [Runbook](0024-seaweedfs/runbook.md) |
| [NoSQL — Cassandra](0025-cassandra/guide.md) | [Guide](0025-cassandra/guide.md), [Policy](0025-cassandra/policy.md), [Runbook](0025-cassandra/runbook.md) |
| [NoSQL — CouchDB](0026-couchdb/guide.md) | [Guide](0026-couchdb/guide.md), [Policy](0026-couchdb/policy.md), [Runbook](0026-couchdb/runbook.md) |
| [NoSQL — MongoDB](0027-mongodb/guide.md) | [Guide](0027-mongodb/guide.md), [Policy](0027-mongodb/policy.md), [Runbook](0027-mongodb/runbook.md) |
| [Operational — MNG-DB](0028-management-database/guide.md) | [Guide](0028-management-database/guide.md), [Policy](0028-management-database/policy.md), [Runbook](0028-management-database/runbook.md) |
| [Operational — Supabase](0029-supabase/guide.md) | [Guide](0029-supabase/guide.md), [Policy](0029-supabase/policy.md), [Runbook](0029-supabase/runbook.md) |
| [Optimization hardening](0030-optimization-hardening/guide.md) | [Guide](0030-optimization-hardening/guide.md), [Policy](0030-optimization-hardening/policy.md), [Runbook](0030-optimization-hardening/runbook.md) |
| [Relational — PostgreSQL Cluster](0031-postgresql-cluster/guide.md) | [Guide](0031-postgresql-cluster/guide.md), [Policy](0031-postgresql-cluster/policy.md), [Runbook](0031-postgresql-cluster/runbook.md) |
| [PostgreSQL logical upgrade restore rehearsal](0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) | [Runbook](0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md) |
| [Specialized — Neo4j](0033-neo4j/guide.md) | [Guide](0033-neo4j/guide.md), [Policy](0033-neo4j/policy.md), [Runbook](0033-neo4j/runbook.md) |
| [Specialized — Qdrant](0034-qdrant/guide.md) | [Guide](0034-qdrant/guide.md), [Policy](0034-qdrant/policy.md), [Runbook](0034-qdrant/runbook.md) |
| [Storage exhaustion](0035-storage-exhaustion/runbook.md) | [Runbook](0035-storage-exhaustion/runbook.md) |

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
