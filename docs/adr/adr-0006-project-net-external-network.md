# Architecture Decision Record (ADR)

_Target Directory: `docs/adr/adr-0006-project-net-external-network.md`_

## Title: adr-0006: External `project_net` Convention

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Network Architect
- **Deciders:** Platform Team

## 1. Context and Problem Statement

Applications often reside in separate repositories from the core infrastructure. Hardcoding internal Docker bridge IPs is brittle, and exposing every database port to localhost leads to port collisions.

## 2. Decision Drivers

- **Interoperability**: Easy bridging between infra and external apps.
- **Security**: Control which containers can "talk" to the infra network.
- **Simplicity**: Standardized alias names across projects.

## 3. Decision Outcome

**Chosen option: "External `project_net` Bridge"**, because using a pre-existing Docker network with a consistent name allows external projects to connect to infrastructure services (Postgres, Redis, etc.) using stable DNS aliases without exposing them globally.

### 3.1 Core Engineering Pillars Alignment

- **Architecture**: Cleanly separates infrastructure from application lifecycle.
- **Performance**: Native bridge performance over port-forwarding.

### 3.2 Positive Consequences

- Unified discovery mechanism.
- Reduction in host port conflicts.

### 3.3 Negative Consequences

- Requires the network to be manually created once (`docker network create project_net`).

## 5. Confidence Level

- **Confidence Rating**: Medium-High
