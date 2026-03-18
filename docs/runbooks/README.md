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

- [**Deployment Logic**](2026-03-15-deployment-runbook.md) — Standardized rollout and safe rollback paths.
- [**Docker Maintenance**](2026-03-15-docker-resource-maintenance.md) — Managing Docker resources and constraints.
- [**Infra Bootstrap**](2026-03-15-infra-bootstrap-runbook.md) — Environment setup and global recovery.
- [**Incident Response**](2026-03-15-incident-response-runbook.md) — General incident handling protocols.
- [**Monitoring**](2026-03-15-monitoring-runbook.md) — Observability stack health and alerting.

### 🌐 Gateway & Security

- [**Gateway 502 Errors**](2026-03-15-gateway-502-errors.md) — Resolving edge proxy errors.
- [**Traefik Recovery**](2026-03-15-traefik-proxy-recovery.md) — Edge routing remediation.
- [**Auth Lockout**](2026-03-15-auth-lockout.md) — Emergency access procedures.
- [**Vault Sealed**](2026-03-15-vault-sealed.md) — Unsealing protocols and rotation.
- [**Keycloak Restore**](2026-03-15-keycloak-db-restore.md) — Identity provider database recovery.

### 💾 Data & Messaging

- [**Postgres HA**](2026-03-15-postgres-ha-recovery.md) — Patroni cluster recovery.
- [**Valkey Failover**](2026-03-15-valkey-cluster-manual-failover.md) — Key-value store health.
- [**Minio Sync**](2026-03-15-minio-sync-failure.md) — Object storage consistency.
- [**OpenSearch Shard**](2026-03-15-opensearch-shard-recovery.md) — Search cluster maintenance.
- [**Kafka Broker**](2026-03-15-kafka-broker-offline.md) — Stream processing recovery.
- [**Kafka Ops**](2026-03-15-kafka-cluster-ops.md) — Messaging cluster management.

### 🤖 Automation & Observability

- [**Airflow Recovery**](2026-03-15-airflow-celery-recovery.md) — Worker and task reliability.
- [**n8n Recovery**](2026-03-15-n8n-worker-recovery.md) — Low-code automation health.
- [**Observability Maintenance**](2026-03-15-observability-stack-maintenance.md) — LGTN stack upkeep.
- [**Observability Storage**](2026-03-15-observability-storage-full.md) — Handling disk pressure in monitoring.

## 📐 Operational Standards

Every runbook MUST follow the 8-section template from [`../../templates/runbook-template.md`](../../templates/runbook-template.md).

---
> [!IMPORTANT]
> **NO THEORY, ONLY ACTION.** Procedural runbooks save time during outages.

This README is the canonical lazy-load entrypoint for runbook discovery from [`../README.md`](../README.md).
