# Operations Index

This document is the central index for operational readiness in repositories created from this template. It provides policy-level guidance and points to executable runbooks managed by the **DevOps Agent**.

> **IMPORTANT:** Detailed operational procedures, deployment scripts, and incident guides are located exclusively in the `runbooks/` directory. **Never create `docs/runbook` or use an `operations/` folder.**

## 1. Runbook Catalog

All operational procedures must use `templates/operations/runbook-template.md`. Below is the index of standard runbooks included in the `runbooks/` directory.

| Runbook           | Status | Location                                 | Purpose                              |
|-------------------|--------|------------------------------------------|--------------------------------------|
| Deployment        | Active | `runbooks/deployment-runbook.md`         | Staging/Production release steps     |
| Incident Response | Active | `runbooks/incident-response-runbook.md`  | SEV-1/SEV-2 incident mitigation      |
| Monitoring        | Active | `runbooks/monitoring-runbook.md`         | Threshold checks and alerting config |

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

- **Metrics**: Essential RED metrics MUST be collected utilizing OTel collectors, adhering to `.agent/rules/2610-observability-strategy.md`.
- **Logging**: All logs MUST use structured JSON format with correlation IDs per `.agent/rules/2620-logging-std.md`.
- **Tracing**: Critical inter-service pipelines MUST propagate HTTP `trace_id` headers per `.agent/rules/2610-observability-strategy.md`.
- **Alerts**: Alerts trigger based on SLO Error Budget burns affecting users, adhering to `.agent/rules/2630-alerting-std.md`.

## 4. Continuity & Disaster Recovery

- **Data Backups**: All stateful data stores MUST have automated, encrypted daily backups at a minimum, verified monthly, adhering to `.agent/rules/0342-backup-restore.md`.
- **Recovery Time Objective (RTO)**: Target < 4 hours for Tier-1 services.
- **Recovery Point Objective (RPO)**: Target < 1 hour of potential data loss via WAL (Write-Ahead Logging) or continuous replication.

## 5. Operational Rules

### Pre-Deployment Checks

Code must not be deployed unless:

1. Specs in `specs/` exist and are implemented.
2. Reviewer Agent approves the PR.
3. Tests across all tiers pass (unit tests colocated, E2E in global `tests/`) via `.github/workflows/`.
4. A rollback procedure is documented in the corresponding deployment runbook.

### Incident Priorities

- **SEV-1 (Critical)**: Production offline. Immediate action via `runbooks/incident-response-runbook.md` and `.agent/rules/0380-incident-response.md`.
- **SEV-2 (Major)**: Critical flow degraded.
- **SEV-3 (Minor)**: Non-critical bugs.

## 6. Security Baseline

- CI/CD must run `.github/workflows/` container and SAST security scans.
- See `.github/SECURITY.md` for vulnerability policies.

---

> **Note to AI Agents (DevOps Role):** Do not write operation steps directly in this index. For any operational change, modify or create a specific runbook inside `runbooks/` using the approved template.
