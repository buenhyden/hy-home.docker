---
trigger: model_decision
glob: ["OPERATIONS.md", ".github/workflows/*.yml", "**/deployment/**", "**/pipelines/**"]
description: "Operations Blueprint Standards: Requires an OPERATIONS.md defining environments, deploy strategy, observability, backups, and incident response."
---

# Operations Blueprint Standards

- **Role**: SRE / Operations Owner
- **Purpose**: Ensure production operations requirements are documented and consistent so deployments are safe, observable, and recoverable.
- **Activates When**: Planning deployments, configuring CI/CD, or introducing production-impacting changes.

## 1. Standards

### Principles

- **[REQ-OPS-01] Root Blueprint Required**
  - The repository MUST include a root `OPERATIONS.md` that defines environment hierarchy, deploy/release strategy, and continuity targets.
- **[REQ-OPS-02] Spec Alignment**
  - Feature-level Specs MUST declare operational needs (logs/metrics/alerts/backups) consistent with `OPERATIONS.md`.
- **[REQ-OPS-03] Evidence-Based Readiness**
  - Operational readiness MUST be supported by verifiable evidence (CI checks, test results, monitoring dashboards, alert rules).

### Must

- **[REQ-OPS-04] Environment Hierarchy**
  - `OPERATIONS.md` MUST define environments (Dev/Staging/Production) and promotion rules.
- **[REQ-OPS-05] Deployment Strategy**
  - `OPERATIONS.md` MUST define the default deployment strategy (rolling/blue-green/canary) and when to use each.
- **[REQ-OPS-06] Observability Baseline**
  - `OPERATIONS.md` MUST define structured logging requirements and metric/alert baselines, aligned with the Observability pillar (`2600-*`).
- **[REQ-OPS-07] Continuity Plan**
  - `OPERATIONS.md` MUST define backup frequency and retention, and SHOULD define RTO/RPO targets.

### Must Not

- **[BAN-OPS-01] Silent Production Changes**
  - Production-impacting changes MUST NOT be merged without an explicit ops/observability section in the Spec or an approved operational ADR.

## 2. Procedures

- **[PROC-OPS-01] Pre-Deploy Checklist**
  - Before production deployment, confirm: approved Spec, QA sign-off, rollback plan, alert coverage for RED metrics, and backup/restore readiness.
- **[PROC-OPS-02] Post-Deploy Verification**
  - After deployment, verify dashboards/alerts/logs show expected behavior and that error budgets are not rapidly burning.

## 3. Examples

### Good Example (Environment Promotion)

- "Staging: manual approval on tag; Production: manual gate after staging sign-off."

## 4. Validation Criteria

- [ ] **[VAL-OPS-01]** `OPERATIONS.md` exists and defines environments, deploy strategy, observability, and backups.
- [ ] **[VAL-OPS-02]** Specs declare feature-level ops needs and reference `OPERATIONS.md`.
- [ ] **[VAL-OPS-03]** CI/CD includes quality gates before merge/deploy (lint/test/security).
