# Operations Index

This document is the central index for operational readiness in repositories created from this template. It provides policy-level guidance and points to executable runbooks managed by the **DevOps Agent**.

> 1. **Technical Blueprints**: [**Service Technical context hub**](docs/context/README.md).
> 2. **Executable Procedures**: [**Runbooks Catalog**](runbooks/README.md).
> 3. **Infrastructure Hub**: `infra/` (Technical Specs and folder-level READMEs).

## 1. Runbook & Maintenance Catalog

Below is the index of verified operational guides.

| Category | Procedure | Location |
| :--- | :--- | :--- |
| **HA DB** | PostgreSQL HA & Patroni Recovery | [postgres-ha-recovery.md](runbooks/04-data/postgres-ha-recovery.md) |
| **Gateway**| Traefik Ingress & Gateway Recovery | [traefik-proxy-recovery.md](runbooks/01-gateway/traefik-proxy-recovery.md) |
| **Messaging**| Kafka Cluster & KRaft Recovery | [kafka-cluster-ops.md](runbooks/05-messaging/kafka-cluster-ops.md) |
| **Auth** | Keycloak Auth Lockout Recovery | [auth-lockout.md](runbooks/02-auth/auth-lockout.md) |
| **Storage** | MinIO Sync & Read-only Fix | [minio-sync-failure.md](runbooks/04-data/minio-sync-failure.md) |
| **Security**| Vault Unseal & Recovery | [vault-sealed.md](runbooks/03-security/vault-sealed.md) |
| **Monitor** | Observability Stack & Alloy Configuration | [observability-stack-maintenance.md](runbooks/06-observability/observability-stack-maintenance.md) |
| **Workflow**| Airflow Celery Recovery | [airflow-celery-recovery.md](runbooks/07-workflow/airflow-celery-recovery.md) |

> **Note:** If a specific operational procedure (e.g. database migration, failover) is missing from this index, the DevOps Agent should proactively create a new runbook based on `templates/operations/runbook-template.md` and link it here.

## 2. Environment & Deployment Strategy

### Environment Hierarchy

- **Development (Dev)**: Used for intra-team testing. Automatically deployed upon PR merge to `main`.
- **Staging**: Used for pre-production validation (QA, Load testing, User Acceptance). Matches production infrastructure parity exactly.
- **Production**: Live environment for end-users.

### Deployment Strategy

- **Default Strategy**: Blue-Green Deployment (or Rolling Update for stateless worker tiers). Zero-downtime required.
- **Infrastructure Mutability**: Manual "ClickOps" in production is strictly **FORBIDDEN**. All changes must execute via Infrastructure-as-Code (Terraform/ArgoCD).

## 3. Observability Baseline

- **Metrics**: Essential RED metrics MUST be collected utilizing Alloy collectors, adhering to `.agent/rules/2610-observability-strategy.md`.
- **Collection**: Unified OTLP ingestion via [Grafana Alloy](docs/context/06-observability/lgtm-stack-blueprint.md).

## 4. Continuity & Disaster Recovery

- **Data Backups**: All stateful data stores MUST have automated, encrypted daily backups at a minimum, verified monthly, adhering to `.agent/rules/0342-backup-restore.md`.
- **Recovery Time Objective (RTO)**: Target < 4 hours for Tier-1 services.
- **Recovery Point Objective (RPO)**: Target < 1 hour of potential data loss via WAL (Write-Ahead Logging) or continuous replication.

For Docker resource cleanup and WSL volume compression, use the dedicated runbook: `runbooks/core/docker-resource-maintenance.md`.

For a deep overview of infrastructure lifecycle and startup order, see [infra-lifecycle-ops.md](docs/context/core/infra-lifecycle-ops.md).

## 5. Operational Rules

### Pre-Deployment Checks

Code must not be deployed unless:

1. Specs in `specs/` exist and are implemented.
2. Reviewer Agent approves the PR.
3. Tests across all tiers pass (unit tests colocated, E2E in global `tests/`) via `.github/workflows/`.
4. A rollback procedure is documented in the corresponding deployment runbook.

### Incident Priorities

- **SEV-1 (Critical)**: Production offline. Immediate action via `runbooks/core/incident-response-runbook.md` and `.agent/rules/0380-incident-response.md`.
- **SEV-2 (Major)**: Critical flow degraded.
- **SEV-3 (Minor)**: Non-critical bugs.

## 6. Security Baseline

- CI/CD must run `.github/workflows/` container and SAST security scans.
- See `.github/SECURITY.md` for vulnerability policies.

---

> **Note to AI Agents (DevOps Role):** Do not write operation steps directly in this index. For any operational change, modify or create a specific runbook inside `runbooks/` using the approved template.
