---
title: 'ADR-0001: Root Orchestration with include'
status: 'Accepted'
date: '2026-02-26'
authors: 'Platform Architect'
deciders: 'DevOps Team'
---

# Architecture Decision Record (ADR)

## Title: Root Orchestration via `include`

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

- **Security**: Ensures consistent network and volume naming across included files.
- **Observability**: Simplifies mapping of service definitions to infrastructure tiers.
- **Performance**: No measurable overhead for inclusion at runtime.
- **Documentation**: Maps directly to the `infra/` directory structure.

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
- **Technical Requirements Addressed**: REQ-PRD-BASE-01
