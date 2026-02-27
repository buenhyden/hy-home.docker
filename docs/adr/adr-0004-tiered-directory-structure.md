# Architecture Decision Record (ADR)

## Title: Tiered Directory Structure

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Platform Lead
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

A flat directory structure for infrastructure service definitions becomes unmanageable as the number of folders in `infra/` grows. Identifying dependencies and the correct startup sequence becomes difficult for human engineers.

## 2. Decision Drivers

- **Discoverability**: Easy to find service categories (Gateway vs. Data vs. AI).
- **Ordering**: Enforce logical dependency order (01-gateway -> 02-identity -> 04-data).

## 3. Decision Outcome

**Chosen option: "2-Digit Prefixing"**, because organizing `infra/` with numeric tiers provides an intuitive map of system layers and prevents "folder sprawl".

### 3.1 Core Engineering Pillars Alignment

- **Security**: Improves reviewability by making “where a service lives” predictable, reducing accidental cross-tier coupling.
- **Observability**: Clarifies where tier-specific telemetry configs live (e.g., `06-observability`).
- **Compliance**: Supports consistent governance boundaries (what changes affect which tier).
- **Performance**: Reduces operational overhead by improving navigation and dependency clarity.
- **Documentation**: Aligns directory layout with ARD/PRD references and the layered service map in `ARCHITECTURE.md`.
- **Localization**: Not applicable (repository structure).

### 3.2 Positive Consequences

- Clear dependency hierarchy visually.
- Easier onboarding; engineers understand the stack layout at a glance.

### 3.3 Negative Consequences

- Moving a service requires updating the root `docker-compose.yml` include paths (low frequency).

## 4. Alternatives Considered (Pros and Cons)

### Flat Directory

Keep all folders at the top level of `infra/`.

- **Good**, because it is simpler to manage file paths.
- **Bad**, because it lacks any indicator of dependency or hierarchy.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Proven pattern for complex infrastructure-as-code repos.
- **Technical Requirements Addressed**: REQ-PRD-FUN-01

## 6. Related Documents (Traceability)

- **Feature PRD**: [System Architecture Standards PRD](../prd/system-architecture-prd.md)
- **Architecture Reference (ARD)**: [Global System Architecture ARD](../ard/system-architecture-ard.md)
- **Repository Blueprint**: [ARCHITECTURE.md](../../ARCHITECTURE.md)
