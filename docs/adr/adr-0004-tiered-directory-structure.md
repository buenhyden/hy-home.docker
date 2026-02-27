---
title: 'ADR-0004: Tiered Directory Structure'
status: 'Accepted'
date: '2026-02-26'
authors: 'Platform Lead'
deciders: 'DevOps Team'
---

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

- **Architecture**: Reflects the actual layered design of the system.
- **Documentation**: Simplifies tree-based documentation of the repository.

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
- **Technical Requirements Addressed**: REQ-PRD-BASE-04
