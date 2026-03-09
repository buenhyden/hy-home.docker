---
title: '[SPEC-INFRA-01] Infrastructure Global Baseline'
status: 'Validated'
version: '1.0'
owner: 'Platform Architect'
prd_reference: '[infra-baseline-prd.md](../../docs/prd/infra-baseline-prd.md)'
arch_reference: '[system-architecture-ard.md](../../docs/ard/system-architecture-ard.md)'
tags: ['spec', 'implementation', 'baseline']
---

# Implementation Specification (Spec)

> **Status**: Validated
> **Related PRD**: [[PRD-BASE-01] Infrastructure Baseline PRD](../../docs/prd/infra-baseline-prd.md)
> **Related Architecture**: [[ARD-ARCH-01] Global System Architecture](../../docs/ard/system-architecture-ard.md)

_Target Directory: `specs/infra/global-baseline/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

| Item | Check Question | Required | Alignment Notes |
| --- | --- | --- | --- |
| Architecture Style | Is the style Microservices? | Must | Tier-based stack |
| Service Boundaries | Are module boundaries documented? | Must | In ARD-ARCH-01 |
| Backend Stack | Are frameworks decided? | Must | Docker Compose 2.20+ |
| Test Strategy | Levels defined? | Must | Audit-01/02 |

---

## 1. Technical Overview & Architecture Style

This specification establishes the global technical invariants for all infrastructure services. It defines the mandatory inheritance model, least privilege access controls, and environment portability required across the Hy-Home service tiers.

- **Component Boundary**: Global repository baseline.
- **Key Dependencies**: Docker Engine 24.0+, Docker Compose v2.20+.
- **Tech Stack**: YAML, Bash, Docker.

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority | Parent PRD REQ |
| --- | --- | --- | --- |
| **[SPEC-GLOB-01]** | All services MUST extend from `infra/common-optimizations.yml`. | Critical | PRD-BASE-01 |
| **[SPEC-GLOB-02]** | services SHALL utilize `${DEFAULT_DATA_DIR}` for all bind mounts. | Critical | PRD-BASE-01 |
| **[SPEC-GLOB-03]** | Runtime filesystems SHALL be `read_only: true` by default. | High | PRD-BASE-01 |

## 3. Data Modeling & Storage Strategy

- **Database Engine**: N/A (Global Standard).
- **Schema Strategy**: Tiered directory structure with numeric prefixes.
- **Path Abstraction**: Variable `DEFAULT_DATA_DIR` from `.env`.

## 4. Interfaces & Internal API

- **Logging Interface**: Loki driver with `hy-home.tier` and `job` labels.
- **Environment API**: Mandatory `.env` template defined in `.env.example`.

## 5. Component Breakdown

- **`infra/common-optimizations.yml`**: Centralized security, resource, and logging templates.
- **`.env.example`**: Definitive listing of required environment variables.

## 6. Edge Cases & Error Handling

- **Missing ENV**: Startup SHALL fail if `DEFAULT_DATA_DIR` is unbound.
- **Resource Exhaustion**: Services hitting mem_limit SHALL be restarted by the system (unless-stopped).

## 7. Verification Plan (Testing & QA)

- **[VAL-SPEC-001] Audit-01**: Run `docker compose config` to verify template resolution.
- **[VAL-SPEC-002] Audit-02**: Verify label searchability in Grafana Loki Explorer.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Standardization**: 100% of services must use the common optimization templates.

## 9. Operations & Observability

- **Monitoring & Alerts**: Centralized via Loki/Prometheus.
- **Logging**: Mandatory standard metadata labels as defined in Section 4.
- **Data Protection**: Mandatory use of path abstraction for all persistent volumes.
