# Data Tier Documentation (04-data)

> Persistence, Caching, and Storage Services.

## 1. Overview

This directory contains technical guides for the `hy-home.docker` data infrastructure layer (04-data). Documentation is organized by database type to facilitate efficient system management and AI-assisted operations.

## 2. Infrastructure Guides

1. [Relational Databases (SQL)](./01.relational-dbs.md) - PostgreSQL (Standalone/HA) and Supabase.
2. [Cache & Key-Value Stores](./02.cache-kv-dbs.md) - Managed Valkey and Distributed Clusters.
3. [NoSQL Databases](./03.nosql-dbs.md) - MongoDB, Cassandra, and CouchDB.
4. [Object & Distributed Storage](./04.storage-systems.md) - MinIO and SeaweedFS.
5. [Analytical & Specialized Engines](./05.analytical-specialized-dbs.md) - InfluxDB, ksqlDB, OpenSearch, Neo4j, and Qdrant.

## 3. Related Documentation

- [Infrastructure Source](../../../infra/04-data/README.md) - Technical source of truth.
- [Operations Policy](../../08.operations/04-data/README.md) - Governance and backup rules.
- [Recovery Runbooks](../../09.runbooks/04-data/README.md) - Incident response and emergency procedures.

---
Copyright (c) 2026. Licensed under the MIT License.
