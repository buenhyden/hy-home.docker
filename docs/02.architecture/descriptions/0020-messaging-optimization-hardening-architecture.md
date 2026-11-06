---
title: "05-Messaging Optimization Hardening Architecture Description"
version: "1.2.5"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0020"
parent_ids:
- "REQ-0006"
created: "2026-03-28"
---
# 05-Messaging Optimization Hardening Architecture Description

## Overview

### Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `05-messaging` layer. It describes the structure that aligns the
currently implemented Kafka management traffic path with the gateway
standard chain and the authentication boundary, and blocks operational
regression through CI baseline verification.

## Scope

The messaging layer operates the Kafka broker data plane and the management
UI/API plane separately. The management plane applies standard middleware at
the Traefik TLS termination point, and the data plane keeps a service
health-based dependency relationship within the `kafka_net` internal
boundary.

### System Boundaries

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

## Structure

### Architecture

- Kafka:
  - `messaging` profile: `kafka-1`, `schema-registry`, `kafka-connect`, `debezium-db-provision`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`
  - Separate LAB `labs/kafka-cluster/docker-compose.yml` (not promoted): `lab-kafka-1/2/3`, `lab-kafka-exporter`, `lab-kafka-init`; no HOME state is shared
- Gateway Path:
  - Client -> Traefik(`websecure`) -> middleware chain -> management endpoints
- Internal Path:
  - service-to-service traffic over `kafka_net`

## Runtime and Deployment

### Runtime View

- **Key Entities / Flows**:
  - Kafka topics (event/log streams)
- **Storage Strategy**:
  - state data separation based on `${DEFAULT_MESSAGE_BROKER_DIR}`
- **Data Boundaries**:
  - long-term retention/analytics is offloaded to the `04-data` layer

### Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - `messaging` profile: Kafka `kafka-1` single broker with the selected schema/connect/rest/admin configuration
  - Traefik TLS termination + middleware policy
- **Verification**: the registered `infrastructure-hardening` gate in
  `.github/workflow-contract.yml` checks the tracked messaging configuration.

## Quality and Risks

### Quality Attributes

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

## Related Documents

- **Requirement**: [REQ-0006 Messaging](../../01.requirements/0006-messaging.md)
- **Tier Architecture Description**: [AD-0005 Messaging Architecture Description](0005-messaging-architecture.md)
- **ADR**: [ADR-0052 Kafka as the only messaging broker](../decisions/0052-kafka-only-messaging-broker.md)
- **Guide**: [Messaging optimization hardening guide](../../05.operations/guides/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)
- **Policy**: [Messaging optimization hardening policy](../../05.operations/policies/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)
- **Runbook**: [Messaging optimization hardening runbook](../../05.operations/runbooks/06-messaging-and-cdc/0037-messaging-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
