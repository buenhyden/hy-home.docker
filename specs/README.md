# Technical Specifications Hub (`specs/`)

This directory is the absolute **Source of Truth** for the During-Development phase. Every artifact SHALL comply with the `[REQ-SPT]` standards.

## 1. Directory Structure

### 🏗️ Infrastructure Specifications

- **[[SPEC-INFRA-01] Global Baseline](/specs/infra/global-baseline/spec.md)**: Standard templates for `extends` and security invariants.
- **[[SPEC-INFRA-02] Implementation Baseline](/specs/infra/baseline/spec.md)**: Modular orchestration, Day-0 bootstrap, and secrets strategy.
- **[[SPEC-INFRA-03] Automation Logic](/specs/infra/automation/spec.md)**: "Init-Sidecar" implementation and automated resource readiness.
- **[[SPEC-INFRA-04] Hardening & Density](/specs/infra/system-optimization/spec.md)**: Host isolation, aggregate memory limits, and p95 ingestion SLOs.

## 2. Compliance Baseline [REQ-SPT-05]

Every specification in this directory MUST contain:

- **Identifier**: Machine-readable coded ID (e.g., `[SPEC-INFRA-NNN]`).
- **Persona**: Mandatory framing from an engineering persona perspective.
- **Components**: NFR, Storage, Interfaces, Verification, Security, and Ops sections.
- **Verification**: At least 3 testable Given-When-Then Acceptance Criteria [REQ-SPT-10].

---
> [!IMPORTANT]
> **NO SPEC, NO CODE.** All infrastructure modifications MUST BE grounded in an approved specification.
