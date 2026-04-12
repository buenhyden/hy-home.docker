---
layer: agentic
---

# ci-cd-patterns

## Overview

CI/CD deployment strategies, security gate placement, and DORA metrics reference for this workspace. Covers pipeline design from pre-commit to production with Docker Compose-adapted deployment patterns.

## Purpose

Provide a consistent, auditable CI/CD pattern set so pipelines are safe, measurable, and aligned with workspace SLOs.

## Scope

**Covers:**

- Deployment strategy comparison (Rolling, Blue-Green, Canary, Recreate) adapted for Docker Compose + Traefik
- Security gate placement (pre-commit, PR, build, staging, production)
- Gate tool selection (Gitleaks, Semgrep, Trivy, Syft)
- Vulnerability SLA policy (CVSS-based: Critical ≤24h, High ≤7d, Medium ≤30d, Low ≤90d)
- DORA metrics targets for this workspace (Deployment frequency, Lead time, Change failure rate, Recovery time)
- Branch strategy and deployment mapping

**Excludes:**

- STRIDE/DREAD threat modeling (see container-threat-modeling)
- Detailed SOLID/CWE code review patterns (see code-review-dimensions)

## Structure

- Deployment strategy selection → health check design → gate placement → DORA measurement

## Agents

- **infra-implementer** — deployment pattern caller
- **security-auditor** — gate configuration caller

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger when designing or auditing CI/CD pipelines.
- **Inputs:** deployment target, branch strategy, security requirements
- **Outputs:** pipeline YAML configuration + gate policy document

## Artifacts

- `_workspace/pipeline_<date>.md`
- `_workspace/gate_policy_<date>.md`

## Related Documents

- `../../scopes/infra.md`
- `../../scopes/security.md`
- `../functions/docker-compose-patterns.md`
- `../README.md`
