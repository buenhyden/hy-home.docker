---
title: "Choice of Spilo/Patroni for PostgreSQL HA"
version: "2.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0004"
parent_ids:
- "AD-0004"
created: "2026-03-26"
---

# ADR-0004: Choice of Spilo/Patroni for PostgreSQL HA

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

This document is the architecture decision record for adopting a Patroni and Etcd based high-availability (HA) cluster solution, instead of a single PostgreSQL instance, to guarantee data integrity and uptime for `hy-home.docker`.

- Need to prevent a single point of failure (SPOF) in the data tier.
- Need automated failover and replication-lag monitoring.
- Need flexible cluster configuration and operational convenience in a container environment.

###### Sources
<!-- core-payload-level:4 -->

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

- **PRD**: [../../01.requirements/0004-data.md](../../01.requirements/0004-data.md)
- **Architecture Description**: [../descriptions/0004-data-architecture.md](../01.descriptions/0004-data-architecture.md)

##### Decision Scope

Explicit non-goals:

- Database sharding (out of scope for this ADR).
- Application-level data migration strategy.

#### Options

##### Considered Options

###### Vanilla PostgreSQL with Replication
<!-- core-payload-level:4 -->

- Good: simple configuration and low resource consumption.
- Bad: needs manual failover and replication-lag monitoring is difficult.

###### Postgres Operator (K8s)
<!-- core-payload-level:4 -->

- Good: highly automated in a Kubernetes environment.
- Bad: introduces significant overhead since the current environment is Docker Compose based.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Vanilla PostgreSQL with Replication | Simple configuration and low resource consumption. | Needs manual failover, and replication-lag monitoring is difficult. | Not chosen because it needs manual failover and makes replication-lag monitoring difficult. |
| Postgres Operator (K8s) | Highly automated in a Kubernetes environment. | Introduces significant overhead since the current environment is Docker Compose based. | Not chosen because it adds significant overhead in the current Docker Compose based environment. |
| Spilo (Zalando's PostgreSQL + Patroni) with Etcd | Minimizes data loss and increases uptime on failure with automated failover; Patroni with Etcd gives stable leader election. | Increased resource consumption from the 3-node configuration and complex routing through HAProxy (pg-router); per SPEC-0215 it runs only in the standalone LAB on one host, so it is not host HA. | Selected to meet the drivers of preventing a data-tier SPOF, automated failover and replication-lag monitoring, and flexible cluster configuration in a container environment. |

Vanilla replication was not chosen because it needs manual failover and makes replication-lag monitoring difficult. The Postgres Operator was not chosen because it adds significant overhead in the current Docker Compose based environment.

#### Decision

##### Chosen Option

**Spilo (Zalando's PostgreSQL + Patroni)** is selected for the PostgreSQL HA
topology. SPEC-0215 narrows where it runs: the topology exists only in the
standalone LAB `labs/postgresql-ha/docker-compose.yml`. HOME `mng-pg` and DEV `dev-pg` are
single nodes without failover, and the LAB nodes share one host, so the LAB
exercises replication and failover but is not host HA.

- **Patroni**: works with Etcd to provide stable leader election and automatic failover.
- **Spilo Image**: uses the proven PostgreSQL HA image maintained by Zalando.
- **Etcd**: manages cluster state as a strongly consistent store.

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-26.

#### Consequences

##### Impacts

- **Positive**: minimizes data loss and increases uptime on failure, with automated failover.
- **Trade-offs**: increased resource consumption from the 3-node configuration, and a need for complex routing configuration through HAProxy (pg-router).

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

No follow-up work is recorded in this decision.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
