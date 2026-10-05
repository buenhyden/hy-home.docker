---
title: "Choice of Spilo/Patroni for PostgreSQL HA"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0004"
parent_ids:
- "AD-0004"
created: "2026-03-26"
---
# ADR-0004: Choice of Spilo/Patroni for PostgreSQL HA

## Context

This document is the architecture decision record for adopting a Patroni and Etcd based high-availability (HA) cluster solution, instead of a single PostgreSQL instance, to guarantee data integrity and uptime for `hy-home.docker`.

- Need to prevent a single point of failure (SPOF) in the data tier.
- Need automated failover and replication-lag monitoring.
- Need flexible cluster configuration and operational convenience in a container environment.

### Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision

**Spilo (Zalando's PostgreSQL + Patroni)** is selected as the core database engine.

- **Patroni**: works with Etcd to provide stable leader election and automatic failover.
- **Spilo Image**: uses the proven PostgreSQL HA image maintained by Zalando.
- **Etcd**: manages cluster state as a strongly consistent store.

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Vanilla PostgreSQL with Replication

- Good: simple configuration and low resource consumption.
- Bad: needs manual failover and replication-lag monitoring is difficult.

### Postgres Operator (K8s)

- Good: highly automated in a Kubernetes environment.
- Bad: introduces significant overhead since the current environment is Docker Compose based.

## Consequences

- **Positive**: minimizes data loss and increases uptime on failure, with automated failover.
- **Trade-offs**: increased resource consumption from the 3-node configuration, and a need for complex routing configuration through HAProxy (pg-router).

### Explicit Non-goals

- Database sharding (out of scope for this ADR).
- Application-level data migration strategy.

## Related Documents

- **PRD**: [../../01.requirements/0004-data.md](../../01.requirements/0004-data.md)
- **Architecture Description**: [../descriptions/0004-data-architecture.md](../descriptions/0004-data-architecture.md)
- **Spec**: [../../03.specs/004-data/spec.md](../descriptions/0004-data-architecture.md)
