---
title: '[PRD-BASE-01] Infrastructure Baseline PRD'
status: 'Approved'
version: 'v1.0.0'
owner: 'Platform Architect'
stakeholders: ['DevOps Team', 'Home-Lab Users']
tags: ['prd', 'requirements', 'baseline', 'infra']
---

# [PRD-BASE-01] Infrastructure Baseline PRD

> **Status**: Approved
> **Target Version**: v1.0.0
> **Owner**: Platform Architect
> **Stakeholders**: DevOps Team, Home-Lab Users

_Target Directory: `docs/prd/infra-baseline-prd.md`_

---

## 0. Pre-Review Checklist (Business & Product)

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     | High-level vision established | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     | Bootstrap time < 10 mins     | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     | Enthusiast/Dev/DevOps        | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     | Standard ACs defined         | Section 4   |

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
| **REQ-PRD-MET-02** | Security Coverage | 50%                | 100% (Secrets)   | Audit cycle         |
| **REQ-PRD-MET-03** | Resource Efficiency | N/A                | < 20% Overhead   | Baseline run        |

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

## 6. Technical Specifications

- **Technical Specification**: [Infra Baseline Spec](../../../../../specs/infra/baseline/spec.md)

## 7. Milestones & Roadmap

- **M1: Baseline Setup**: Foundation tiers (Gateway, Data) established.
- **M2: Security Hardening**: 100% secret management logic applied.

## 8. Risks, Security & Compliance

- **Risks**: Resource exhaustion on low-RAM hosts.
- **Security**: Mandatory `cap_drop` and `no-new-privileges`.
