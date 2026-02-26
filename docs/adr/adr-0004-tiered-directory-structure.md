# Architecture Decision Record (ADR)

_Target Directory: `docs/adr/adr-0004-tiered-directory-structure.md`_

## Title: adr-0004: Tiered Directory Structure

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Platform Lead
- **Deciders:** DevOps Team

## 1. Context and Problem Statement

A flat directory structure for infrastructure service definitions becomes unmanageable as the number of folders in `infra/` grows.

## 2. Decision Drivers

- **Discoverability**: Easy to find service categories.
- **Ordering**: Enforce logical dependency order (Gateway -> Auth -> Data).

## 3. Decision Outcome

**Chosen option: "2-Digit Prefixing"**, because organizing `infra/` with numeric tiers (e.g., `01-gateway`, `04-data`) provides an intuitive map of system layers.

### 3.1 Core Engineering Pillars Alignment

- **Architecture**: Reflects the layered design of the system.

### 3.2 Positive Consequences

- Clear dependency hierarchy visually.
- Easier onboarding for new engineers.

### 3.3 Negative Consequences

- Moving a service requires updating the root `docker-compose.yml` include paths.

## 5. Confidence Level

- **Confidence Rating**: High
