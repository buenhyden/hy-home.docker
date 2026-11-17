---
title: "05-Messaging Optimization Hardening Architecture Description"
version: "1.4.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0020"
parent_ids:
- "REQ-0006"
created: "2026-03-28"
---

# 05-Messaging Optimization Hardening Architecture Description

## Context and Boundaries

### System Boundary

The HOME messaging data plane uses the internal `kafka_net`. Kafbat uses
Traefik TLS and the gateway standard chain with native Keycloak OIDC.
The standalone LAB has its own broker, Schema Registry and Connect
interfaces on `lab_kafka_net`.

- **Owns**:
  - Messaging management path routing/middleware contract
  - Kafka UI image version pinning policy
  - Messaging hardening baseline verification (CI + script)
  - optimization-hardening document traceability
- **Consumes**:
  - `01-gateway` Traefik middleware chain
  - `02-auth` SSO scheme
  - `06-observability` metrics/alerts
- **Does Not Own**:
  - Producer/consumer application implementation
  - Non-messaging tier infrastructure configuration
- **Non-goals**:
  - Immediate multi-region/multi-cluster migration
  - App-level reprocessing code implementation

#### Purpose and Readers

This document defines the optimization/hardening reference architecture of
the `05-messaging` layer. It describes the structure that aligns the
currently implemented Kafka management traffic path with the gateway
standard chain and the authentication boundary, and blocks operational
regression through CI baseline verification.

#### Context

HOME uses the `01-gateway` middleware chain, `02-auth` Keycloak OIDC and
`06-observability` metrics and alerts. Any downstream persistent store or
analytics pipeline belongs to its consumer.

### Constraints

Security requires TLS and native OIDC on the HOME management route and
pinned images. This architecture does not introduce a multi-region HOME
topology. The linked policy and runbook own operational checks and recovery.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

## Structure

### Building Blocks

- HOME `messaging` selects `kafka-1`, `kafbat-ui`, `kafka-exporter` and
  `kafka-init`. Kafbat is the gateway management route.
- The separate `lab-kafka` profile declares three LAB brokers, exporter,
  init, Schema Registry and Connect. Its CDC endpoints stay on the LAB
  network and carry no configured source connector.

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| HOME management path (Traefik `websecure` to Kafbat) | Kafbat (`kafbat-ui`) behind Traefik | Browser users | `01-gateway` gateway standard chain with native Keycloak OIDC | The linked [Messaging optimization hardening runbook](../../05.operations/runbooks/06-messaging-and-cdc/0037-messaging-optimization-hardening.md) owns recovery. |
| Internal broker listeners on `kafka_net` | HOME broker `kafka-1` | HOME containers | The description links no contract for this interface. | Healthchecks order dependent starts; the single HOME broker provides no redundancy and the linked runbook owns recovery. |
| PLAINTEXT EXTERNAL listener on loopback | HOME broker `kafka-1` | Loopback clients on the host | The description links no contract for this interface. | The description records no failure handling for this interface. |
| JMX exporter on loopback and `obs_net` | HOME broker `kafka-1` | `06-observability` metrics and alerts | The description links no contract for this interface. | The description records no failure handling for this interface. |
| LAB broker, Schema Registry and Connect on `lab_kafka_net` | `lab-kafka` profile from `labs/kafka-cluster/docker-compose.yml` | LAB containers | The description links no contract for this interface. | The description records no failure handling for this interface. |
| SSO scheme | `02-auth` Keycloak | Kafbat | Native Keycloak OIDC | The description records no failure handling for this interface. |

- HOME management path: browser → Traefik (`websecure`) → Kafbat → Keycloak OIDC.
- Containers use the internal broker listeners on `kafka_net` in HOME or
  `lab_kafka_net` in the LAB. The HOME broker also joins `obs_net` and
  publishes its PLAINTEXT EXTERNAL listener and JMX exporter on loopback.
  LAB Schema Registry and Connect have no HOME gateway route.

## Runtime Behavior

### Normal Flow

#### Runtime View

- **Key Entities / Flows**:
  - Kafka topics (event/log streams)
- **Storage Strategy**:
  - HOME broker state uses `${DEFAULT_MESSAGE_BROKER_DIR}`; LAB broker
    state uses `${LAB_DATA_DIR}`.
- **Data Boundaries**:
  - Broker topic state stays in its project. Consumers own downstream
    retention and processing.

#### Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - The root `messaging-broker` and `messaging-admin` profiles select narrower
    HOME subsets. HOME declares neither the former REST proxy nor CDC services.
  - The independent LAB starts from `labs/kafka-cluster/docker-compose.yml`.
- **Verification**: the registered `infrastructure-hardening` gate in
  `.github/workflow-contract.yml` checks the tracked messaging configuration.

### Failure and Recovery

Healthchecks order dependent starts. The single HOME broker provides no broker
redundancy. The linked runbook owns recovery and its separate evidence.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Performance**: burst traffic control and transient-failure absorption
  through the gateway standard chain
- **Security**: TLS and native OIDC on Kafbat, LAB-internal CDC endpoints and
  pinned images.
- **Reliability**: health-gated dependencies and explicit state boundaries.
  Authentication, failover and restore require separate runtime evidence.
- **Observability**: linkage of compose health + exporter metrics + CI
  evidence
- **Operability**: a single operational contract kept through standard
  scripts + runbook + policy documents

### Trade-offs

- HOME runs a single broker and accepts that it provides no broker redundancy;
  the linked runbook owns recovery and its separate evidence (Failure and
  Recovery).
- The architecture does not introduce a multi-region HOME topology, and
  multi-region or multi-cluster migration is a non-goal (Constraints, System
  Boundary).
- Health-gated dependencies and explicit state boundaries are kept, while
  authentication, failover and restore still require separate runtime
  evidence (Quality Attributes).
- LAB Schema Registry and Connect stay on `lab_kafka_net` without a HOME
  gateway route, and their CDC endpoints carry no configured source connector
  (Building Blocks, Interfaces).

## Decisions and Adoption

### Decisions

- **ADR**: [ADR-0052 Kafka as the only messaging broker](../decisions/0052-kafka-only-messaging-broker.md)
- **ADR**: [ADR-0062 HOME and LAB placement](../decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- **Requirement**: [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)

#### Currentness and Lineage

The description reflects the current tree at its `updated` date and history lives in Git.

- **Tier Architecture Description**: [AD-0005 Messaging Architecture Description](0005-messaging-architecture.md)
- **Guide**: [Messaging optimization hardening guide](../../05.operations/guides/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)
- **Policy**: [Messaging optimization hardening policy](../../05.operations/policies/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)
- **Runbook**: [Messaging optimization hardening runbook](../../05.operations/runbooks/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)
