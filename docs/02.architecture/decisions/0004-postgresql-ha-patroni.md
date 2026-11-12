---
title: "Choice of Spilo/Patroni for PostgreSQL HA"
version: "1.1.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0004"
parent_ids:
- "AD-0004"
created: "2026-03-26"
---
# ADR-0004: Choice of Spilo/Patroni for PostgreSQL HA

## Context

### Problem and Drivers

This document is the architecture decision record for adopting a Patroni and Etcd based high-availability (HA) cluster solution, instead of a single PostgreSQL instance, to guarantee data integrity and uptime for `hy-home.docker`.

- Need to prevent a single point of failure (SPOF) in the data tier.
- Need automated failover and replication-lag monitoring.
- Need flexible cluster configuration and operational convenience in a container environment.

### Decision Scope

Explicit non-goals:

- Database sharding (out of scope for this ADR).
- Application-level data migration strategy.

## Decision

### Chosen Option

**Spilo (Zalando's PostgreSQL + Patroni)** is selected for the PostgreSQL HA
topology. SPEC-0215 narrows where it runs: the topology exists only in the
standalone LAB `labs/postgresql-ha/docker-compose.yml`. HOME `mng-pg` and DEV `dev-pg` are
single nodes without failover, and the LAB nodes share one host, so the LAB
exercises replication and failover but is not host HA.

- **Patroni**: works with Etcd to provide stable leader election and automatic failover.
- **Spilo Image**: uses the proven PostgreSQL HA image maintained by Zalando.
- **Etcd**: manages cluster state as a strongly consistent store.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-26.

## Alternatives

### Considered Options

#### Vanilla PostgreSQL with Replication

- Good: simple configuration and low resource consumption.
- Bad: needs manual failover and replication-lag monitoring is difficult.

#### Postgres Operator (K8s)

- Good: highly automated in a Kubernetes environment.
- Bad: introduces significant overhead since the current environment is Docker Compose based.

### Trade-offs

Vanilla replication was not chosen because it needs manual failover and makes replication-lag monitoring difficult. The Postgres Operator was not chosen because it adds significant overhead in the current Docker Compose based environment.

## Consequences

### Impacts

- **Positive**: minimizes data loss and increases uptime on failure, with automated failover.
- **Trade-offs**: increased resource consumption from the 3-node configuration, and a need for complex routing configuration through HAProxy (pg-router).

### Follow-up

No follow-up work is recorded in this decision.

## Traceability

### Sources

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

- **PRD**: [../../01.requirements/0004-data.md](../../01.requirements/0004-data.md)
- **Architecture Description**: [../descriptions/0004-data-architecture.md](../descriptions/0004-data-architecture.md)
