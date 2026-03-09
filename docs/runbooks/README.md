# Operational Runbooks Hub (`runbooks/`)

This directory is the **exclusive, authoritative home** for all executable procedures and incident response guides. Every file here is strictly procedural and follows the mandatory 8-section structure defined in `[REQ-RBK-STR-01]`.

## 📚 Documentation Taxonomy

1. **Architecture Reference (ARD)** ([`docs/ard/`](../docs/ard/README.md)): "How it's built".
2. **Product Requirements (PRD)** ([`docs/prd/`](../docs/prd/README.md)): "What it should do".
3. **Operational Runbooks** ([`runbooks/`](./README.md)): "What to type" during an incident.

## 🧭 Operational Navigator (Role-Based)

### 🏗️ For Platform Engineers (Bootstrap & Core)

- [**Core Procedures**](core/infra-bootstrap-runbook.md) — Environment setup, `docker compose` bootstrap, and global recovery.
- [**Deployment Logic**](core/deployment-runbook.md) — Standardized rollout and safe rollback paths.
- [**Gateway Ingress**](01-gateway/traefik-proxy-recovery.md) — Traefik routing and edge service remediation.
- [**Security & Vault**](03-security/vault-sealed.md) — Unsealing protocols and rotation scripts.

### 💾 For Data & Reliability Engineers

- [**Database HA**](04-data/postgres-ha-recovery.md) — PostgreSQL Patroni clusters and data consistency.
- [**Search & Cache**](04-data/opensearch-shard-recovery.md) — OpenSearch health and Valkey cluster failovers.
- [**Observability Stack**](06-observability/observability-stack-maintenance.md) — Maintaining Loki, Grafana, and Prometheus.

### 🤖 For AI & Automation Ops

- [**Workflow Engines**](07-workflow/airflow-celery-recovery.md) — Airflow workers and n8n job reliability.

## 📐 Operational Standards

Every runbook MUST follow the 8-section template from [`templates/operations/runbook-template.md`](../templates/operations/runbook-template.md):

1. **Service Overview** (Owners/Criticality)
2. **Dependencies** (Upstream impact)
3. **Dashboards & SLOs** (Where to look)
4. **Common Failures** (GIVEN-WHEN-THEN scenarios)
5. **Rollback Procedure** (How to revert)
6. **Data Safety** (Stateful considerations)
7. **Escalation Path** (Who to page)
8. **Verification Steps** (How to confirm fix)

---
> [!IMPORTANT]
> **NO THEORY, ONLY ACTION.** Procedural runbooks save time during outages. Background info belongs in `docs/`.
