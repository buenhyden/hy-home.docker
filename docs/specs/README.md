---
layer: core
---

# Technical Specifications Hub (`specs/`)

This directory is the tactical source of truth for active implementation contracts. All specifications are categorized by infrastructure tiers and functional domains.

## Specification Families

### 🏗️ Global & Agent Standards

- [**Agent Instruction Refactor**](agent-instructions-spec.md) — Normalizing agent guidance.
- [**Global Baseline**](infra-global-baseline-spec.md) — Cross-stack standards and conventions.
- [**Service Standards**](infra-service-standards-spec.md) — Inter-service communication rules.

### 🛠️ Infrastructure Core

- [**Implementation Baseline**](infra-baseline-spec.md) — Core foundation requirements.
- [**Automation Logic**](infra-automation-spec.md) — Autonomous operations specifications.
- [**Secrets Bootstrap**](infra-secrets-bootstrap-spec.md) — Initial zero-trust setup.
- [**System Optimization**](infra-system-optimization-spec.md) — Hardening and resource density.

### 📊 Platform Services

- [**AI Services**](infra-ai-spec.md) — Local inference and vector storage.
- [**Observability Stack**](infra-observability-spec.md) — LGTM stack implementation details.
- [**Messaging Fabric**](infra-messaging-spec.md) — Kafka and stream processing.

## Compliance Baseline

Every specification in this directory MUST contain:

- **Identifier**: Machine-readable coded ID (e.g., `[SPEC-INFRA-001]`).
- **Verification**: At least 3 testable Given-When-Then Acceptance Criteria.

---
> [!IMPORTANT]
> **NO SPEC, NO CODE.** All infrastructure modifications MUST be grounded in an approved specification.
