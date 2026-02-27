---
title: '[PRD-BASE-01] Infrastructure Baseline PRD'
status: 'Approved'
version: 'v1.0.0'
owner: 'Platform Architect'
stakeholders: 'DevOps Team, Home-Lab Users'
tags: ['prd', 'requirements', 'baseline', 'infra']
---

# [PRD-BASE-01] Infrastructure Baseline PRD

> **Status**: Approved
> **Target Version**: v1.0.0
> **Owner**: Platform Architect
> **Stakeholders**: DevOps Team, Home-Lab Users

_Target Directory: `docs/prd/infra-baseline-prd.md`_
_Note: This document defines the What and Why for the core infrastructure foundations._

---

## 0. Pre-Review Checklist (Business & Product)

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     | High-level vision established | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     | Bootstrap time < 10 mins     | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     | Enthusiast/Dev/DevOps        | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     | Standard ACs defined         | Section 4   |
| Scope (In)            | Is the feature list included in this release clearly defined?          | Must     | Foundation tiers defined    | Section 5   |
| Not in Scope          | Is what we will NOT build in this release explicitly listed?           | Must     | Out-of-scope defined        | Section 6   |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated?                          | Must     | M1/M2 defined               | Section 7   |
| Risks & Compliance    | Are major risks, privacy, or regulatory constraints documented?        | Must     | Low-RAM risk documented     | Section 8   |

---

## 1. Vision & Problem Statement

**Vision**: To provide a highly modular, secure, and production-grade local infrastructure for DevOps experimentation and home-lab hosting using Docker Compose.

**Problem Statement**: Local infrastructure is often fragmented, insecure, and difficult to reproduce, leading to wasted time on setup instead of learning or development.

## 2. Target Personas

- **Persona 1 (Home-Lab Enthusiast)**:
  - **Pain Point**: Complex multi-service setups break easily.
  - **Goal**: A stable environment that is easy to bootstrap.
- **Persona 2 (DevOps Engineer)**:
  - **Pain Point**: Testing infra patterns locally is hard without standard layering.
  - **Goal**: A sandbox that mirrors production-grade orchestration and security.

## 3. Success Metrics (Quantitative)

| ID                 | Metric Name        | Baseline (Current) | Target (Success) | Measurement Period  |
| ------------------ | ------------------ | ------------------ | ---------------- | ------------------- |
| **REQ-PRD-MET-01** | Bootstrap Time     | 30 mins            | < 10 mins        | Day-0 build         |
| **REQ-PRD-MET-02** | Security Coverage  | 50%                | 100% (Secrets)   | Audit cycle         |
| **REQ-PRD-MET-03** | Resource Efficiency | N/A                | < 4GB Idle (RAM) | Baseline run        |
| **REQ-PRD-MET-04** | Build Latency      | > 5 mins           | < 2 mins (Hot)   | CI/CD build cycle   |

## 4. Key Use Cases & Acceptance Criteria (GWT)

| ID           | User Story (INVEST)                                                                      | Acceptance Criteria (Given-When-Then)                                                                                                |
| ------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **STORY-01** | **As a** Enthusiast,<br>**I want** a preflight check,<br>**So that** I know I'm missing secrets. | **Given** a clean Docker environment,<br>**When** running `preflight-compose.sh`,<br>**Then** missing secrets are identified. |

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]** Modular Orchestration via `include`.
- **[REQ-PRD-FUN-02]** Secrets-First Policy enforcement (100% Docker Secrets).
- **[REQ-PRD-FUN-03]** Bootstrap Prerequisites: Define required `.env` keys and directory permissions.
- **[REQ-PRD-FUN-04]** Local TLS Standardisation via `mkcert` (secrets/certs/).
- **[REQ-PRD-FUN-05]** Centralized Log Aggregation using Loki.
- **[REQ-PRD-FUN-06]** Global Configuration Inheritance via `infra/common-optimizations.yml`.
- **[REQ-PRD-FUN-07]** Mandatory `extends` usage for cross-file resource and security baseline.

## 6. Out of Scope

- Application-level logic and business features.
- External cloud provider integration (AWS/GCP/Azure).
- Deployment to Kubernetes or cluster schedulers beyond Docker Compose.

## 7. Milestones & Roadmap

- **M1: Baseline Setup**: Foundation tiers (Gateway, Data) established.
- **M2: Security Hardening**: 100% secret management logic applied.

## 8. Risks, Security & Compliance

- **Risks**: Resource exhaustion on low-RAM hosts.
- **Security**: Mandatory `cap_drop` and `no-new-privileges` enforced via `common-optimizations.yml`.
- **Compliance**: Adherence to local security standards for local environment sandboxing.

## 9. Assumptions & Dependencies

- **Assumptions**: Host system has Docker Engine (v20.10+) and Docker Compose (v2.20+) installed.
- **Dependencies**: RELIES on correct `.env` configuration for path mapping.

## 10. Q&A / Open Issues

- **[ISSUE-01]**: Should we support rootless Docker? - **Update**: Deferred to Phase 3.

## 11. Related Documents (Reference / Traceability)

- **Technical Specification**: [[SPEC-INFRA-01] Infrastructure Global Baseline Specification](/specs/infra/global-baseline/spec.md)
- **Architecture Decisions (ADRs)**: [[ADR-0001] Root Orchestration via include](../adr/adr-0001-root-orchestration-include.md)
