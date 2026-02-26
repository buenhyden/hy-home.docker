# Architecture Decision Record (ADR)

_Target Directory: `docs/adr/adr-0001-root-orchestration-include.md`_

## Title: adr-0001: Root Orchestration with `include`

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Platform Architect
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

Managing 30+ services in a single `docker-compose.yml` is unmaintainable and prone to merge conflicts as the infrastructure scales.

## 2. Decision Drivers

- **Scalability**: Need to manage a growing number of services.
- **Maintainability**: Clear separation of service definitions.
- **Developer Experience**: Reduce "wall of YAML" fatigue.

## 3. Decision Outcome

**Chosen option: "Docker Compose `include`"**, because it allows the root `docker-compose.yml` to serve as a registry, importing service-specific Compose files from `infra/` while maintaining unified lifecycle management.

### 3.1 Core Engineering Pillars Alignment

- **Architecture**: Enforces modular service management.
- **Documentation**: Maps directly to the `infra/` directory structure.

### 3.2 Positive Consequences

- Modular service management.
- Cleaner diffs and isolated tiers.

### 3.3 Negative Consequences

- Requires Docker Compose v2.20+.

## 4. Alternatives Considered

### Monolithic Compose File

- **Good**: Zero dependency on file includes.
- **Bad**: Becomes unreadable and error-prone at scale.

## 5. Confidence Level

- **Confidence Rating**: High
- **Notes**: Standard pattern for large Compose projects.
