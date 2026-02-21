---
trigger: model_decision
glob: ["**/*.{tf,yaml,yml,dockerfile,json}", "**/Dockerfile"]
description: "DevOps Pillar Standard. Enforces Immutable Infrastructure (IaC), Declarative Systems, and SRE Observability (SLO/SLI)."
---

# 0300-DevOps-Pillar

- **Role**: DevOps Engineer / SRE
- **Purpose**: Enforce immutable, declarative, and observable infrastructure standards.
- **Activates When**: Managing Infrastructure, CI/CD, Containers, or Observability.

## 1. Standards

### 1.1 Core Principles

- **[REQ-OPS-IMM-01] Immutability**: Servers MUST NOT be patched; they MUST be replaced ("Cattle, not Pets").
- **[REQ-OPS-IAC-01] Declarative**: All infrastructure MUST be defined in code (Terraform/K8s/Docker). Manual "ClickOps" is FORBIDDEN.
- **[REQ-OPS-OBS-01] Observable**: Systems MUST emit Metrics (Prometheus), Logs (JSON), and Traces by default.

### 1.2 Configuration Management

- **[REQ-OPS-CFG-01] External Config**: App config MUST be injected via ENV vars or Secret Stores.
- **[REQ-OPS-SEC-01] Secrets**: Secrets MUST NEVER be committed to git. Use Vault/KMS/GitHub Secrets.

### 1.3 SRE & Reliability

- **[REQ-SRE-SLO-01] SLO Definition**: Critical services MUST have Service Level Objectives (e.g., "99.9% Availability").
- **[REQ-SRE-ERR-01] Error Budgets**: Deployments MUST halt if Error Budgets are exhausted.

### 1.4 Containerization

- **[REQ-OPS-DOC-01] Base Images**: Use specific tags (e.g., `node:18-alpine`), NEVER `latest`.
- **[REQ-OPS-DOC-02] Least Privilege**: Containers MUST run as non-root users.

## 2. Procedures

### 2.1 Infrastructure Lifecycle

1. **Code**: Define resources in Terraform/Helm.
2. **Plan**: Run `terraform plan` or `kubectl diff`.
3. **Review**: Validate changes against policy (OPA/Sentinel).
4. **Apply**: Execute via CI/CD pipeline (No local apply).

### 2.2 SRE Alerting Workflow

1. **Indicator (SLI)**: Define success metric (e.g., Latency < 200ms).
2. **Objective (SLO)**: Define target (e.g., 99% of requests).
3. **Alert**: Trigger PagerDuty only on Budget Burn (User Impact), not CPU spikes (Symptoms).

## 3. Examples

### 3.1 Terraform Best Practice

```hcl
# Good: Remote State with Locking
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "prod/app"
    dynamodb_table = "terraform-locks"
  }
}
```

### 3.2 Docker Security

```dockerfile
# Good: Non-root user
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN addgroup -S app && adduser -S app -G app
USER app
CMD ["node", "index.js"]
```

## 4. Validation Criteria

- [ ] **[VAL-OPS-IAC-01]** No manual console changes allowed.
- [ ] **[VAL-OPS-SEC-01]** Secrets are properly managed.
- [ ] **[VAL-OPS-SLO-01]** SLOs are defined for production services.
- [ ] **[VAL-OPS-DOC-01]** Dockerfiles run as non-root.
