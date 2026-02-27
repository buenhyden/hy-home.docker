# Architecture Decision Record (ADR)

## Title: Removing Static Docker IPs

- **Status:** Accepted
- **Date:** 2026-02-23
- **Authors:** Platform Engineer
- **Deciders:** Infrastructure Team

## 1. Context and Problem Statement

The initial infrastructure composition designated static IPv4 addresses for crucial containers via the centralized `infra_net` bridge. While static IPs simplified external routing in legacy designs, in modern Docker environments, hardcoding static IPs is an anti-pattern. It restricts deployment to single instances and risks IP collisions.

## 2. Decision Drivers

- **Scalability**: Need to support multiple stack instances on one host.
- **Predictability**: Rely on Docker's native lifecycle for network provisioning.
- **Best Practices**: Eliminate brittle hardcoded networking dependencies.

## 3. Decision Outcome

**Chosen option: "Docker Internal DNS"**, because removing explicit `ipv4_address` assignments and relying exclusively on container names or aliases allows for higher portability and avoids network boot race conditions.

### 3.1 Core Engineering Pillars Alignment

- **Security**: Avoids brittle addressing patterns that encourage bypassing ingress/auth layers via “known IPs”.
- **Observability**: Improves portability of dashboards/runbooks by referencing stable DNS names (service names) instead of per-host IP tables.
- **Compliance**: Reduces configuration drift risk across environments (no hardcoded IP registries).
- **Performance**: Docker’s internal DNS is efficient and avoids manual IP management overhead.
- **Documentation**: Standardizes docs on service DNS and hostnames, preventing “static IP” drift.
- **Localization**: Not applicable (networking convention).

### 3.2 Positive Consequences

- **Highly Portable**: The stack can be spun up on different subnets without modification.
- **Resilient**: Avoids race conditions where an IP hasn't been released gracefully.

### 3.3 Negative Consequences

- **DNS Exclusivity**: Ad-hoc commands or scripts that previously hardcoded these internal IPs will break.

## 4. Alternatives Considered (Pros and Cons)

### Static IP Addressing (Legacy)

Manually assign every service an IP in the subnet.

- **Good**, because routing is predictable for legacy external systems.
- **Bad**, because it's brittle and prevents scaling horizontally.

## 5. Confidence Level & Technical Requirements

- **Confidence Rating**: High
- **Notes**: Moving toward standard cloud-native networking patterns.
- **Technical Requirements Addressed**: REQ-PRD-SYS-MET-04, REQ-PRD-SYS-FUN-05

## 6. Related Documents (Traceability)

- **Feature PRD**: [System Optimization PRD](../prd/system-optimization-prd.md)
- **Feature Spec**: [System Optimization Spec](../../specs/infra/system-optimization/spec.md)
- **Repository Blueprint**: [ARCHITECTURE.md](../../ARCHITECTURE.md)
