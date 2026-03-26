---
tier: 08.operations
component: 06-observability
title: Loki Operational Policy
status: production
updated: 2026-03-26
---

# Loki Operational Policy

> Operational standards for the Loki log aggregation system.

## 1. Data Retention Policy

To balance storage costs and operational needs, the following retention periods are enforced:

- **Standard Application Logs**: 7 Days (168h).
- **Security & Audit Logs**: 30 Days.
- **System Infrastructure Logs**: 7 Days.

> [!IMPORTANT]
> Retention is enforced by the Loki Compactor. Data older than the specified period is permanently deleted from MinIO.

## 2. Label Governance (Cardinality)

High cardinality labels can degrade Loki performance and increase storage costs.

- **Mandatory Labels**: `service_name`, `env`, `stream` (stdout/stderr).
- **Prohibited Labels**: User IDs, IP addresses, Request IDs, or any high-cardinality dynamic data.
- **Best Practice**: Use `LogQL` parsers (e.g., `| json`) to extract dynamic fields at query time instead of using them as labels.

## 3. Performance & Resource Standards

- **Batching**: Alloy must batch log entries (min 1s or 256KB) before pushing to Loki.
- **Ingester Memory**: `infra-loki` container is limited to 2GB RAM. Monitor `loki_ingester_memory_chunks_bytes` to prevent OOM.
- **Compaction**: The compactor runs every 10 minutes to optimize chunk storage in MinIO.

## 4. Backup & Disaster Recovery

- **Config Backup**: `infra/06-observability/loki/config/` is version-controlled.
- **Data Persistence**: MinIO buckets should be backed up using bucket replication or snapshots if long-term audit compliance is required.

---
[System Guide](../../07.guides/06-observability/loki.md) | [Recovery Runbook](../../09.runbooks/06-observability/loki.md)
