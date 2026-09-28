---
title: "05-Messaging Optimization Hardening Architecture Description"
version: "1.2.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0020"
parent_ids:
- "REQ-0006"
created: "2026-03-28"
---
# 05-Messaging Optimization Hardening Architecture Description

## Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `05-messaging` layer. It describes the structure that aligns the
currently implemented Kafka management traffic path with the gateway
standard chain and the authentication boundary, and blocks operational
regression through CI baseline verification.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded
in this section and the following views. Only concerns confirmed in the
existing document are covered here.

The messaging layer operates the Kafka broker data plane and the management
UI/API plane separately. The management plane applies standard middleware at
the Traefik TLS termination point, and the data plane keeps a service
health-based dependency relationship within the `kafka_net` internal
boundary.

## System Boundaries

This section preserves the system boundary, consumption relationships,
non-goals, and constraints already recorded in the current document.

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

## Quality Attributes

### Quality Scenarios

The quality scenarios point to the existing configuration, failure boundary,
and verification expectation to which the attributes below apply. Concrete
execution evidence is owned by the related Spec and Operations documents.

- **Performance**: burst traffic control and transient-failure absorption
  through the gateway standard chain
- **Security**: TLS termination + SSO protection + floating-tag prohibition
- **Reliability**: availability kept through healthcheck dependency and a
  rolling recovery procedure
- **Scalability**: catalog-based readiness for DLQ/reprocessing/quorum queue
  expansion
- **Observability**: linkage of compose health + exporter metrics + CI
  evidence
- **Operability**: a single operational contract kept through standard
  scripts + runbook + policy documents

## Components

### Viewpoints and Views

The context, component, or deployment representation in this section serves
as the view for that concern.

- Kafka:
  - `messaging` profile: `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`
  - When `messaging-cluster` is added to this: `kafka-1/2/3`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`
- Gateway Path:
  - Client -> Traefik(`websecure`) -> middleware chain -> management endpoints
- Internal Path:
  - service-to-service traffic over `kafka_net`

### AI Agent Architecture

- **Model/Provider Strategy**: N/A
- **Tooling Boundary**: messaging changes must pass hardening/document
  traceability verification
- **Memory & Context Strategy**: pins Spec/Plan/Runbook/Catalog links as
  execution context
- **Guardrail Boundary**: prohibits floating tags, unverified middleware
  changes, and ungrounded exposure expansion
- **Latency / Cost Budget**: managed in the operational policy

## Data Flow

### Data and Control Flows

The data and control flows include only the interactions specified in this
section and the existing infrastructure/deployment descriptions.

- **Key Entities / Flows**:
  - Kafka topics (event/log streams)
- **Storage Strategy**:
  - state data separation based on `${DEFAULT_MESSAGE_BROKER_DIR}`
- **Data Boundaries**:
  - long-term retention/analytics is offloaded to the `04-data` layer

## Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - `messaging` profile: Kafka `kafka-1` single broker with the selected schema/connect/rest/admin configuration
  - When `messaging-cluster` is added: the same file's Kafka 3-broker model. Standalone file validation needs the root network/secret context
  - Traefik TLS termination + middleware policy
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 05-messaging`
  - The `infrastructure-hardening` job in `.github/workflows/ci-quality.yml`

## Traceability

The disposition of the parent requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [../01.requirements/0006-messaging.md](../../01.requirements/0006-messaging.md)
- **Spec**: [../03.specs/006-messaging/spec.md](0005-messaging-architecture.md)
- **ADR**: [../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/05-messaging/optimization-hardening.md](../../05.operations/guides/0037-messaging-optimization-hardening.md)
- **Policy**: [../../05.operations/policies/05-messaging/optimization-hardening.md](../../05.operations/policies/0037-messaging-optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/05-messaging/optimization-hardening.md](../../05.operations/runbooks/0037-messaging-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
