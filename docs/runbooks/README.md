---
layer: infra
---

# Operational Runbooks Hub (`runbooks/`)

This directory is the **exclusive, authoritative home** for all executable procedures and incident response guides. Every file here is strictly procedural and follows the mandatory 8-section structure defined in `[REQ-RBK-STR-01]`.

## 📚 Documentation Taxonomy

1. **Architecture Reference (ARD)** ([`../ard/README.md`](../ard/README.md)): "How it's built".
2. **Product Requirements (PRD)** ([`../prd/README.md`](../prd/README.md)): "What it should do".
3. **Operational Runbooks** ([`README.md`](README.md)): "What to type" during an incident.

## 🧭 Operational Navigator

### 🏗️ Platform & Core

- [**Deployment Logic**](deployment-runbook.md) — Standardized rollout and safe rollback paths.
- [**Docker Maintenance**](docker-resource-maintenance.md) — Managing Docker resources and constraints.
- [**Infra Bootstrap**](infra-bootstrap-runbook.md) — Environment setup and global recovery.
- [**Incident Response**](incident-response-runbook.md) — General incident handling protocols.
- [**Monitoring**](monitoring-runbook.md) — Observability stack health and alerting.

### 🌐 Gateway & Security

- [**Gateway 502 Errors**](gateway-502-errors.md) — Resolving edge proxy errors.
- [**Traefik Recovery**](traefik-proxy-recovery.md) — Edge routing remediation.
- [**Auth Lockout**](auth-lockout.md) — Emergency access procedures.
- [**Vault Sealed**](vault-sealed.md) — Unsealing protocols and rotation.
- [**Keycloak Restore**](keycloak-db-restore.md) — Identity provider database recovery.

### 💾 Data & Messaging

- [**Postgres HA**](postgres-ha-recovery.md) — Patroni cluster recovery.
- [**Valkey Failover**](valkey-cluster-manual-failover.md) — Key-value store health.
- [**Minio Sync**](minio-sync-failure.md) — Object storage consistency.
- [**OpenSearch Shard**](opensearch-shard-recovery.md) — Search cluster maintenance.
- [**Kafka Broker**](kafka-broker-offline.md) — Stream processing recovery.
- [**Kafka Ops**](kafka-cluster-ops.md) — Messaging cluster management.

### 🤖 Automation & Observability

- [**Airflow Recovery**](airflow-celery-recovery.md) — Worker and task reliability.
- [**n8n Recovery**](n8n-worker-recovery.md) — Low-code automation health.
- [**Observability Maintenance**](observability-stack-maintenance.md) — LGTN stack upkeep.
- [**Observability Storage**](observability-storage-full.md) — Handling disk pressure in monitoring.

## 📐 Operational Standards

Every runbook MUST follow the 8-section template from [`../../templates/runbook-template.md`](../../templates/runbook-template.md).

---
> [!IMPORTANT]
> **NO THEORY, ONLY ACTION.** Procedural runbooks save time during outages.

This README is the canonical lazy-load entrypoint for runbook discovery from [`../README.md`](../README.md).
