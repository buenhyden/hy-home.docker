---
title: 'Infrastructure Baseline Implementation Spec'
status: 'Implementation'
version: '1.0'
owner: 'Platform Architect'
prd_reference: '../../../docs/prd/infra-baseline-prd.md'
api_reference: 'N/A'
arch_reference: '../../../docs/ard/infra-baseline-ard.md'
tags: ['spec', 'implementation', 'infra', 'baseline']
---

# Implementation Specification: Infrastructure Baseline (Phase 1)

> **Status**: Implementation
> **Related PRD**: [infra-baseline-prd.md](../../../docs/prd/infra-baseline-prd.md)
> **Related ARD**: [infra-baseline-ard.md](../../../docs/ard/infra-baseline-ard.md)

_Target Directory: `specs/infra/baseline/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Modular Compose | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | `infra/<domain>` | Section 1 |
| Quality / Testing  | Test Strategy defined?                                | Must     | GWT scenarios | Section 5 |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | OAuth for Grafana | Section 4 |

---

## 1. Technical Overview & Architecture Style

This specification governs the core setup and security hardening of the primary infrastructure engine. It facilitates modularity via the `include` pattern and enforces zero-plaintext secrets.

- **Component Boundary**: Root `docker-compose.yml` and foundational files.
- **Tech Stack**: Docker Compose v2.20+, YAML, Docker Secrets.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-BAS-001** | Implement `include` pattern for sub-compose imports | Critical | REQ-PRD-FUN-01 |
| **REQ-SPC-BAS-002** | Add `no-new-privileges:true` and `cap_drop: [ALL]` | Critical | REQ-PRD-FUN-01 |
| **REQ-SPC-BAS-003** | Standardize Bootstrap & Secrets Prerequisites | High | REQ-PRD-FUN-03 |
| **REQ-SPC-BAS-004** | Standardize Local TLS paths (secrets/certs/) | High | REQ-PRD-FUN-04 |

## 3. Data Modeling & Storage Strategy

- **Persistence**: 100% bind-mount usage pointing to `${DEFAULT_DATA_DIR}`.
- **Secrets Management**: Mounted via read-only file system at `/run/secrets/`.

## 4. Interfaces & Data Structures

- **Orchestration Interface**: Root compose file acts as a registry for tiered folders (`01-gateway` through `06-observability`).
- **Security Interface**: Mandatory mounting of `.txt` secret files for all Tier-1 data services.

## 5. Acceptance Criteria (GWT)

### REQ-SPC-BAS-001: Registry Persistence

- **Given**: A complex multi-tier setup.
- **When**: Running `docker compose config`.
- **Then**: All service definitions are merged into a single logical stack without duplication.

### REQ-SPC-BAS-002: Hardening Verification

- **Given**: A running container.
- **When**: Executing `cat /proc/1/status | grep Cap`.
- **Then**: The effective capability set is empty (zeros).

### REQ-SPC-BAS-003: Bootstrap Readiness

- **Given**: A clean host.
- **When**: Executing `preflight-compose.sh`.
- **Then**: Missing `.env` keys or `secrets/` files are flagged with exit 1.

## 6. Component Breakdown

- **`docker-compose.yml`**: Root orchestration logic.
- **`infra/**/*.yml`**: Service definitions with baseline security.

## 8. Non-Functional Requirements (NFR)

- **Security Density**: 100% of services must have zero elevated privileges.
- **Bootstrap Latency**: First-time `config` validation must execute in < 2s.

## 9. Operations & Observability

- **Backup Strategy**: Daily snapshot of `${DEFAULT_DATA_DIR}`.
- **Credential Rotation**: Handled via file replacement in `secrets/`.
