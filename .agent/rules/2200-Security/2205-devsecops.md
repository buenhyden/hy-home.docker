---
trigger: model_decision
glob: ["**/*"]
description: "DevSecOps Standards: Enforces security as code, automated testing integrations, and continuous compliance monitoring."
---

# DevSecOps Standards

- **Role**: DevSecOps Architect
- **Purpose**: Define standards for integrating security automation and compliance monitoring across the CI/CD pipeline.
- **Activates When**: Configuring CI/CD workflows, infrastructure as code (IaC), or containerization assets.

**Trigger**: model_decision — Apply during infrastructure and pipeline design.

## 1. Standards

### Principles

- **[REQ-DSO-01] Security as Code**
  - Security policies and infrastructure configurations MUST be defined as version-controlled code.
- **[REQ-DSO-02] Continuous Compliance**
  - Automated compliance checks MUST run on every pull request to ensure zero regression in security posture.
- **[REQ-DSO-03] Modular Isolation**
  - Build environments and production artifacts MUST be isolated to prevent lateral movement and supply chain attacks.

### Pipeline Controls

| Stage | Tooling Example | Core Standard |
| --- | --- | --- |
| Static Analysis | SonarQube / Snyk | SAST pass required |
| Dependency Audit | Dependabot / npm audit | Zero High/Critical vulns |
| Docker Build | Trivy / Hadolint | Non-root users only |
| IaC | Checkov / tfsec | Policy enforcement |

### Must

- **[REQ-DSO-04] Mandatory SCA Audit**
  - Every build MUST perform Software Composition Analysis (SCA) to identify third-party vulnerabilities.
- **[REQ-DSO-05] Infrastructure Scanning**
  - Infrastructure-as-code (Terraform/CloudFormation) MUST be scanned for misconfigurations (e.g., open S3 buckets) before apply.
- **[REQ-DSO-06] Secret Leakage Guard**
  - Pipelines MUST include a secret scanning step (e.g., gitleaks) to prevent credentials from entering the VCS.

### Must Not

- **[BAN-DSO-01] Manual Environment Changes**
  - Direct, manual modification of infrastructure in production is PROHIBITED (must go through IaC).
- **[BAN-DSO-02] Root Container Execution**
  - Application containers MUST NOT run as the `root` user in production environments.

### Failure Handling

- **Stop Condition**: Stop the deployment pipeline if any "Critical" security vulnerability is identified in the artifacts or code.

## 2. Procedures

- **[PROC-DSO-01] Image Hardening**
  - IF creating a new Dockerfile THEN MUST use a verified minimal base image (e.g., Alpine/Distroless).
- **[PROC-DSO-02] Policy Update**
  - Update OPA or Checkov policies monthly to align with the latest industry security benchmarks (e.g., CIS).

## 3. Examples

### Secure Dockerfile (Good)

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
USER node
CMD ["node", "index.js"]
```

## 4. Validation Criteria

- **[VAL-DSO-01] Vulnerability Pass**
  - [ ] CI pipeline logs show 100% pass rate for SAST and SCA scans.
- **[VAL-DSO-02] Non-Root Verification**
  - [ ] Runtime audits confirm that the application process is not running as UID 0.
- **[VAL-DSO-03] Secret Audit**
  - [ ] A deep history scan confirms no private keys or tokens are resident in the `.git` directory.
