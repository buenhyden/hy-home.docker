---
layer: infra
---
# ADR 0001: Root Orchestration via `include`
**Overview (KR):** Docker Compose의 `include` 지연 로딩 기능을 활용하여 인프라 설계를 모듈화하고 관리 효율성을 높이는 결정입니다.

: Root Orchestration via `include`

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Platform Architect
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Managing 30+ services in a single `docker-compose.yml` is unmaintainable and prone to merge conflicts as the infrastructure scales. The cognitive load for developers navigating a monolithic file is high.

## 2. Decision Drivers

- **Scalability**: Need to manage a growing number of services without unpreadable complexity.
- **Maintainability**: Clear separation of service definitions for easier updates.
- **Developer Experience**: Reduce "wall of YAML" fatigue and enable modular interaction.

## 3. Decision Outcome

**Chosen option: "Docker Compose `include`"**, because it allows the root `docker-compose.yml` to serve as a registry, importing service-specific Compose files from `infra/` while maintaining unified lifecycle management and shared networking.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Centralizes shared primitives (networks, secrets, common templates) so included stacks cannot silently diverge from security baselines.
- **Observability**: Makes it easier to enforce and audit common logging/labels by routing all stacks through a single root entrypoint.
- **Compliance**: Supports policy enforcement at one layer (root compose), reducing “hidden overrides” in per-service compose files.
- **Performance**: No runtime performance impact; improves operational performance by reducing merge conflicts and human error.
- **Documentation**: Mirrors the tiered `infra/**` layout and keeps the root entrypoint as the single canonical “what runs” registry.
- **Localization**: Not applicable (infrastructure orchestration policy).

### 3.2 Positive Consequences

- Modular service management and cleaner git diffs.
- Ability to restart or update tiers in isolation without affecting the global config.

### 3.3 Negative Consequences

- Requires Docker Compose v2.20+ (breaking change for legacy installs).

## 4. Alternatives Considered (Pros and Cons)

### Monolithic Compose File

Maintain everything in one file.

- **Good**, because zero dependency on file includes; works on older Docker versions.
- **Bad**, because it becomes unreadable and error-prone at scale; constant merge conflicts.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Standard pattern for large modern Compose projects.
- **Technical Requirements Addressed**: REQ-PRD-BSL-FUN-01, REQ-PRD-OPT-FUN-04

## 6. Related Documents (Traceability)

- **Feature PRD**: [Infrastructure Baseline PRD](../prd/2026-02-27-infra-baseline-prd.md), [System Optimization PRD](../prd/2026-02-26-system-optimization-prd.md)
- **Feature Spec**: [Infrastructure Baseline Spec](../specs/2026-02-27-infra-baseline-spec.md), [System Optimization Spec](../specs/2026-02-26-infra-system-optimization-spec.md)
- **Architecture Reference (ARD)**: [Global System Architecture ARD](../ard/2026-02-26-system-architecture-ard.md)
