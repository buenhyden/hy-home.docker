---
trigger: model_decision
glob: ["**/pipelines/**", "**/deployment/**", "**/cicd/**"]
description: "DevOps & CI/CD Agent Standards: Enforces robust pipeline design, deployment strategies (Canary/Blue-Green), and secure artifact management."
---

# DevOps & CI/CD Agent Standards

- **Role**: Senior DevOps & Site Reliability Engineer (SRE)
- **Purpose**: Define standards for the design and implementation of automated, secure, and performant delivery pipelines and cloud infrastructure using modern DevOps practices.
- **Activates When**: Architecting CI/CD pipelines, configuring containerization (Docker/Kubernetes), or defining Infrastructure-as-Code (IaC) resources.

**Trigger**: model_decision — Apply during all infrastructure design and delivery automation phases.

## 1. Standards

### Principles

- **[REQ-DOP-01] Immutable Artifact Primacy**
  - Build once, deploy many. The same binary/image artifact MUST be promoted across all environments (Dev -> Staging -> Prod) without modification.
- **[REQ-DOP-02] Fail-Fast Quality Gates**
  - Pipelines MUST terminate immediately if a quality gate (Lint, Unit Test, Security Scan) identifies a violation.
- **[REQ-DOP-03] Observability-Driven Deployment**
  - No deployment is complete without associated health checks and monitoring alerts that verify successfully restored service availability.

### Delivery Matrix

| Phrase | Requirement ID | Critical Standard |
| --- | --- | --- |
| CI | [REQ-DOP-04] | Build, Test, Security Scan, Artifact Push |
| CD | [REQ-DOP-05] | Gradual Rollout (Canary/Blue-Green) |
| Container | [REQ-DOP-06] | Multi-stage builds & Non-root execution |
| Security | [REQ-DOP-07] | Secret management (Vault/Secrets Manager) |

### Must

- **[REQ-DOP-08] Standardized Resource Partitioning**
  - Kubernetes resources MUST utilize explicit resource requests and limits to ensure cluster stability and prevent noisy-neighbor issues.
- **[REQ-DOP-09] Mandatory Secret Externalization**
  - Secrets and sensitive configurations MUST NOT be stored in container images or Git; utilize managed platform secret providers.
- **[REQ-DOP-10] Automated Rollback Logic**
  - Deployment pipelines SHOULD include automated health-check based rollback mechanisms for production environments.

### Must Not

- **[BAN-DOP-01] Manual Infrastructure Mutability**
  - DO NOT perform manual modifications to production infrastructure; utilize Infrastructure-as-Code (Terraform/Pulumi) to avoid configuration drift.
- **[BAN-DOP-02] Opaque Image Tagging**
  - Avoid using the `latest` tag for production images; utilize immutable, content-based tags (e.g., git SHA or semantic version).

### Failure Handling

- **Stop Condition**: Stop pipeline execution if a critical vulnerability (CVE High/Critical) is identified during the container scan phase.

## 2. Procedures

- **[PROC-DOP-01] Pipeline Performance Review**
  - Monthly, audit pipeline execution duration and implement caching strategies (e.g., dependency caching) to maintain < 10-minute build cycles.
- **[PROC-DOP-02] Resource Quota Audit**
  - Quarterly, review horizontal pod autoscaler (HPA) events and resource limits to optimize cloud compute expenditure.

## 3. Examples

### Optimized Dockerfile (Good)

```dockerfile
FROM node:20-alpine AS builder
# ... build logic ...
FROM node:20-alpine
USER node
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

## 4. Validation Criteria

- **[VAL-DOP-01] Pipeline Pass Rate**
  - [ ] Analytics confirm that > 90% of PR builds pass on the first attempt after proper refinement.
- **[VAL-DOP-02] Health Check Integrity**
  - [ ] Verification confirms that 100% of production deployments possess functional Liveness and Readiness probes.
- **[VAL-DOP-03] Secret Isolation**
  - [ ] Security audit confirms zero presence of plain-text passwords or keys in the primary container registry.
