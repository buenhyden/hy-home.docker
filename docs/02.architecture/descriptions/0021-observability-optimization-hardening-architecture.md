---
title: "06-Observability Optimization Hardening Architecture Description"
version: "1.0.5"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0021"
parent_ids:
- "REQ-0007"
created: "2026-03-28"
---
# 06-Observability Optimization Hardening Architecture Description

## Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `06-observability` layer. It organizes the gateway boundary security,
health-based dependency, custom image runtime hardening, and catalog-based
expansion strategy from an architecture perspective.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded
in this section and the following views. Only concerns confirmed in the
existing document are covered here.

The observability layer operates the data plane (collection/storage) and the
management plane (UI/API) separately. The management plane applies the
standard middleware+SSO chain at the Traefik TLS termination point, and the
data plane is kept over `obs_net` internal communication.

## System Boundaries

This section preserves the system boundary, consumption relationships,
non-goals, and constraints already recorded in the current document.

- **Owns**:
  - Observability service routing/authentication boundary contract
  - health-based boot order and runtime hardening contract
  - observability hardening verification automation contract
- **Consumes**:
  - `01-gateway` Traefik middleware chain
  - `02-auth` Keycloak-based SSO
  - `04-data` SeaweedFS object storage
- **Does Not Own**:
  - Application instrumentation code (OTel SDK)
  - Non-observability tier routing policy
- **Non-goals**:
  - Immediate multi-cluster/multi-region observability adoption
  - Full redesign of the sampling policy

## Quality Attributes

### Quality Scenarios

The quality scenarios point to the existing configuration, failure boundary,
and verification expectation to which the attributes below apply. Concrete
execution evidence is owned by the related Spec and Operations documents.

- **Performance**: burst control/overload mitigation through the gateway
  standard chain
- **Security**: TLS termination + SSO + non-root container execution
- **Reliability**: improved boot stability through `service_healthy`
  dependency
- **Scalability**: readiness for catalog-based expansion (sampling/retention/
  long-term storage)
- **Observability**: cAdvisor health, pyroscope availability, and stack health validation
- **Operability**: script-based regression blocking + standard runbook
  procedure

## Components

### Viewpoints and Views

The context, component, or deployment representation in this section serves
as the view for that concern.

- Storage/Query Plane:
  - Prometheus, Loki, Tempo, Pyroscope
- Control/Presentation Plane:
  - Grafana, Alertmanager, Pushgateway, Alloy UI, cAdvisor route, Pyroscope route
- Gateway Path:
  - Client -> Traefik(`websecure`) -> `gateway-standard-chain` + `sso-*` -> target service
- Internal Path:
  - OTLP/log/trace traffic over `obs_net`

## Data Flow

### Data and Control Flows

The data and control flows include only the interactions specified in this
section and the existing infrastructure/deployment descriptions.

- **Key Entities / Flows**:
  - Metrics, logs, traces, profiles
- **Storage Strategy**:
  - Prometheus local TSDB
  - Loki/Tempo object storage via SeaweedFS
  - Pyroscope local storage
- **Data Boundaries**:
  - the long-term retention policy is managed at the operations layer

## Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - single-node observability core + optional horizontal expansion
- **Operational Evidence**:
  - `scripts/hardening/check-all-hardening.sh 06-observability`
  - CI `infrastructure-hardening` job

## Evolution

- Prometheus: scrape budget + remote_write tiering
- Loki: label cardinality budget + separate retention/compactor operation
- Tempo: per-service/endpoint sampling policy + span-burst protection
- Alloy: onboarding templating + modularized collection pipeline

## Traceability

The disposition of the parent requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Spec**: [../03.specs/007-observability/spec.md](0006-observability-architecture.md)
- **ADR**: [../02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md](../decisions/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/06-observability/optimization-hardening.md](../../05.operations/guides/0044-observability-optimization-hardening.md)
- **Policy**: [../../05.operations/policies/06-observability/optimization-hardening.md](../../05.operations/policies/0044-observability-optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/06-observability/optimization-hardening.md](../../05.operations/runbooks/0044-observability-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
