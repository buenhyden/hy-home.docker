# Architecture Decision Record (ADR)

## Title: Mandatory Resource Limits

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Site Reliability Engineer
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Local workstations often freeze or experience "thrashing" when 20+ containers start simultaneously without bounds. A single memory leak in one service (e.g., OpenSearch or Kafka) can crash the entire Docker engine and the host OS.

## 2. Decision Drivers

- **Stability**: Prevent system-wide resource exhaustion on development hardware.
- **Predictability**: Ensure services have the memory they actually need to run correctly.
- **Observability**: Clearly define what "normal" resource usage looks like for each tier.

## 3. Decision Outcome

**Chosen option: "Unified Resource Reservations"**, because standardizing `deploy.resources.reservations` and `limits` in every Compose file ensures a floor for essential services and a ceiling for bursty ones, preventing OOM cascades.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Reduces “runaway container” blast radius and supports safer multi-tenant local hosts.
- **Observability**: Makes resource usage expectations explicit and measurable (limits/reservations become the baseline for debugging).
- **Compliance**: Standardizes operational constraints for all long-running services (auditable configuration).
- **Performance**: Prevents noisy-neighbor effects and host thrashing during parallel startups.
- **Documentation**: Ensures resource expectations are documented in code (compose) rather than tribal knowledge.
- **Localization**: Not applicable (runtime constraints).

### 3.2 Positive Consequences

- Stable local environment for multitasking developers.
- Faster detection of memory leaks (containers will restart/restart-policy).

### 3.3 Negative Consequences

- Containers might fail to start if the host is truly out of RAM (strict fail-fast).

## 4. Alternatives Considered (Pros and Cons)

### No Limits (Default)

Let Docker and the OS handle allocation dynamically.

- **Good**, because it is zero-config and flexible.
- **Bad**, because it causes kernel panic or UI lag on shared workstations when one service goes rogue.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Industry standard for reliable container deployments.
- **Technical Requirements Addressed**: REQ-PRD-BASE-MET-03, REQ-PRD-BASE-FUN-08

## 6. Related Documents (Traceability)

- **Feature PRD**: [Infrastructure Baseline PRD](../prd/infra-baseline-prd.md)
- **Feature Spec**: [Infrastructure Baseline Spec](../../specs/infra/baseline/spec.md)
- **Related Specs**: [System Optimization Spec](../../specs/infra/system-optimization/spec.md)
