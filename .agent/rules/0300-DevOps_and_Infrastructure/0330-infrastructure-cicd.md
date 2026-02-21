---
trigger: model_decision
glob: [".github/workflows/*.yml", "**/.github/workflows/*.yml"]
description: "CI/CD: GitHub Actions standards, Workflow hygiene, and Quality Gates."
---

# 0330-Infrastructure-CICD

- **Role**: DevOps Engineer
- **Purpose**: Ensure automated, reliable, and secure software delivery pipelines.
- **Activates When**: Writing GitHub Actions workflows or defining CI/CD pipelines.

## 1. Standards

### 1.1 Principles

- **[REQ-CICD-GEN-01] Fail Fast**: Pipelines MUST fail at the earliest possible stage (lint > test > build).
- **[REQ-CICD-GEN-02] Immutable Artifacts**: Build once, deploy everywhere.
- **[REQ-CICD-GEN-03] Isolation**: Jobs MUST run in isolated environments (containers).

### 1.2 Scope

- **In-Scope**: GitHub Actions, CircleCI, Jenkins configuration.
- **Out-of-Scope**: Application code logic.

### 1.3 Inputs & Outputs

- **Inputs**: Code commits, PRs.
- **Outputs**: Verified artifacts (Docker images), Deployments.

### 1.4 Must / Must Not

- **[REQ-CICD-SEC-01] Secrets**: Secrets MUST be injected via `{{ secrets.XYZ }}` environment variables.
- **[REQ-CICD-PER-01] Caching**: Dependency caching MUST be enabled.
- **[BAN-CICD-SEC-01] No 3rd Party Actions**: Use ONLY allow-listed Actions (official or internal).

## 2. Procedures

### 2.1 Pipeline Stages

1. **Lint**: Check formatting and style.
2. **Test**: Run Unit and Integration tests.
3. **Build**: Compile/Pack artifacts.
4. **Scan**: Security analysis (SAST, Container Scanning).
5. **Deploy**: Progressive delivery to environments.

### 2.2 Quality Gates

- **Code Coverage**: Must meet >80% threshold.
- **Vulnerabilities**: Zero critical/high CVEs.
- **Performance**: No regression in key metrics.

## 3. Examples

### 3.1 Standard GitHub Action

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

## 4. Validation Criteria

- [ ] **[VAL-CICD-SEC-01]** No secrets printed in logs.
- [ ] **[VAL-CICD-GEN-01]** Workflow uses pinned action versions.
- [ ] **[VAL-CICD-GEN-02]** Caching is implemented.

## 5. References

- Related: [0310-infrastructure-docker.md](./0310-infrastructure-docker.md)
