---
title: "06-Observability Optimization Hardening Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0021"
parent_ids:
- "REQ-0007"
created: "2026-03-28"
---

# 06-Observability Optimization Hardening Architecture Description

## Context and Boundaries

### System Boundary

The observability layer separates collection and storage from management
UI and API routes. Traefik terminates TLS for management routes, which use
the gateway chain and route-specific authentication. Internal service flows
use `obs_net`.

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

#### Purpose and Readers

This document defines the optimization/hardening reference architecture of
the `06-observability` layer. It organizes the gateway boundary security,
health-based dependency, custom image runtime hardening, and catalog-based
expansion strategy from an architecture perspective.

#### Context

The layer consumes the `01-gateway` Traefik middleware chain, `02-auth` Keycloak-based SSO and `04-data` SeaweedFS object storage; clients reach management routes through Traefik.

### Constraints

Security requires TLS termination, SSO or application authentication per route, and non-root container execution; boot order is health-based. The long-term retention policy is managed at the operations layer, and multi-cluster/multi-region adoption and a full sampling-policy redesign are non-goals.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

## Structure

### Building Blocks

- Storage/Query Plane:
  - Prometheus, Loki, Tempo, Pyroscope
- Control/Presentation Plane:
  - Grafana, Gatus, Dozzle, Alertmanager, Pushgateway, Alloy UI, cAdvisor route, Pyroscope route
- Exporters:
  - node-exporter, cAdvisor, dcgm-exporter
- Gateway Path:
  - Traefik `websecure` applies `gateway-standard-chain` to management routes.
    Grafana, Gatus and Dozzle use native Keycloak OIDC. Dozzle additionally
    applies its admin IP allowlist. The Prometheus API applies
    `prometheus-api-auth`, and other browser routes use ForwardAuth.
- Internal Path:
  - OTLP/log/trace traffic over `obs_net`

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Gateway management routes (Traefik `websecure`) | Grafana, Gatus, Dozzle, Alertmanager, Pushgateway, Alloy UI, cAdvisor route and Pyroscope route | Browser clients | `gateway-standard-chain` with route-specific authentication: native Keycloak OIDC, Dozzle admin IP allowlist or ForwardAuth | The description records no failure handling for this interface. |
| Prometheus API route | Prometheus | API clients through Traefik | `prometheus-api-auth` | The description records no failure handling for this interface. |
| Internal OTLP/log/trace path on `obs_net` | Instrumented services and exporters | Observability storage and query plane | The description links no contract for this interface. | The data plane is kept over `obs_net` internal communication with `service_healthy` dependency ordering. |
| SSO | `02-auth` Keycloak | Observability management routes | Keycloak-based SSO | The description records no failure handling for this interface. |
| Object storage | `04-data` SeaweedFS | Loki and Tempo | The description links no contract for this interface. | The description records no failure handling for this interface. |

- Gateway path: apply the route-specific authentication listed under Building
  Blocks. Native OIDC and Prometheus API authentication do not use the
  browser ForwardAuth chain.
- Internal path: OTLP/log/trace traffic over `obs_net`.

## Runtime Behavior

### Normal Flow

#### Runtime View

- **Key Entities / Flows**:
  - Metrics, logs, traces, profiles
- **Storage Strategy**:
  - Prometheus local TSDB
  - Loki/Tempo object storage via SeaweedFS
  - Pyroscope local storage
- **Data Boundaries**:
  - the long-term retention policy is managed at the operations layer

#### Deployment View

- **Runtime / Platform**:
  - Docker Compose + `infra/common-optimizations.yml`
- **Deployment Model**:
  - single-node observability core + optional horizontal expansion
- **Verification**:
  - the registered `infrastructure-hardening` gate in `.github/workflow-contract.yml`

### Failure and Recovery

The data plane is kept over `obs_net` internal communication, and boot stability is improved through `service_healthy` dependency. The description records no failure boundary beyond the linked operations documents under Interfaces.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Performance**: burst control/overload mitigation through the gateway
  standard chain
- **Security**: TLS termination, SSO or application authentication per route, and non-root container execution
- **Reliability**: improved boot stability through `service_healthy`
  dependency
- **Scalability**: readiness for catalog-based expansion (sampling/retention/
  long-term storage)
- **Observability**: cAdvisor health, pyroscope availability, and stack health validation
- **Operability**: script-based regression blocking + standard runbook
  procedure

### Trade-offs

- The layer runs a single-node observability core with only optional
  horizontal expansion; multi-cluster or multi-region adoption is a non-goal
  (Deployment View, System Boundary).
- A full sampling-policy redesign is a non-goal, and long-term retention is
  left to the operations layer rather than this architecture (Constraints,
  Data Boundaries).
- Boot stability comes from `service_healthy` dependency ordering, and the
  description records no failure boundary beyond the linked operations
  documents (Failure and Recovery).

## Decisions and Adoption

### Decisions

- **ADR**: [ADR-0021 Observability hardening and HA expansion](../decisions/0021-observability-hardening-and-ha-expansion-strategy.md)

### Adoption Boundaries

#### Requirement Mapping

- **Requirement**: [REQ-0007 Observability](../../01.requirements/0007-observability.md)

#### Currentness and Lineage

- **Tier Architecture Description**: [AD-0006 Observability Architecture Description](0006-observability-architecture.md)
- **Guide**: [Observability optimization hardening guide](../../05.operations/guides/07-observability/0044-observability-optimization-hardening.md)
- **Policy**: [Observability optimization hardening policy](../../05.operations/policies/07-observability/0044-observability-optimization-hardening.md)
- **Runbook**: [Observability optimization hardening runbook](../../05.operations/runbooks/07-observability/0044-observability-optimization-hardening.md)

#### Evolution

- Prometheus: scrape budget + remote_write tiering
- Loki: label cardinality budget + separate retention/compactor operation
- Tempo: per-service/endpoint sampling policy + span-burst protection
- Alloy: onboarding templating + modularized collection pipeline
