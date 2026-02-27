---
title: 'ADR-0006: External project_net Convention'
status: 'Accepted'
date: '2026-02-26'
authors: 'Network Architect'
deciders: 'Platform Team'
---

# Architecture Decision Record (ADR)

## Title: External `project_net` Convention

- **Status:** Accepted
- **Date:** 2026-02-26
- **Authors:** Network Architect
- **Deciders:** Platform Team

## 1. Context and Problem Statement

Applications often reside in separate repositories from the core infrastructure. Hardcoding internal Docker bridge IPs is brittle, and exposing every database port to localhost leads to port collisions. We need a way for external projects to reliably reach shared infrastructure services.

## 2. Decision Drivers

- **Interoperability**: Easy bridging between infra and external apps without exposure.
- **Security**: Control which containers can "talk" to the infra network.
- **Simplicity**: Standardized DNS alias names across disconnected projects.

## 3. Decision Outcome

**Chosen option: "External `project_net` Bridge"**, because using a pre-existing Docker network with a consistent name allows external projects to connect to infrastructure services using stable DNS aliases without exposing them globally.

### 3.1 Core Engineering Pillars Alignment

- **Architecture**: Cleanly separates infrastructure from application lifecycle.
- **Security**: Aligns with network isolation principles.
- **Performance**: Native bridge performance over port-forwarding.
- **Documentation**: Standardized naming reduces documentation overhead for individual projects.

### 3.2 Positive Consequences

- Unified discovery mechanism for all development tools.
- Dramatic reduction in host port conflicts.

### 3.3 Negative Consequences

- Requires the network to be manually created once on the host.

## 4. Alternatives Considered (Pros and Cons)

### Global Network (Infra_net)

Connect all external apps directly to the internal infra network.

- **Good**, because it is extremely simple.
- **Bad**, because it breaks isolation; external apps could see all internal metrics/logs backends.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Common pattern for platform-as-a-service styles.
- **Technical Requirements Addressed**: REQ-PRD-AUTO-01, REQ-PRD-BASE-06
