---
title: "06-Observability Optimization Hardening Architecture Description"
version: "1.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "AD-0021"
parent_ids:
- "REQ-0007"
created: "2026-03-28"
---

# 06-Observability Optimization Hardening Architecture Description

## Overview

### Purpose and Readers

This document defines the optimization/hardening reference architecture of
the `06-observability` layer. It organizes the gateway boundary security,
health-based dependency, custom image runtime hardening, and catalog-based
expansion strategy from an architecture perspective.

### System Boundary

The observability layer operates the data plane (collection/storage) and the
management plane (UI/API) separately. The management plane applies the
standard middleware+SSO chain at the Traefik TLS termination point, and the
data plane is kept over `obs_net` internal communication.

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

## Context and Constraints

### Context

The layer consumes the `01-gateway` Traefik middleware chain, `02-auth` Keycloak-based SSO and `04-data` SeaweedFS object storage; clients reach management routes through Traefik.

### Constraints

Security requires TLS termination, SSO or application authentication per route, and non-root container execution; boot order is health-based. The long-term retention policy is managed at the operations layer, and multi-cluster/multi-region adoption and a full sampling-policy redesign are non-goals.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

## Current Structure

### Building Blocks

- Storage/Query Plane:
  - Prometheus, Loki, Tempo, Pyroscope
- Control/Presentation Plane:
  - Grafana, Gatus, Alertmanager, Pushgateway, Alloy UI, cAdvisor route, Pyroscope route
- Exporters:
  - node-exporter, cAdvisor, dcgm-exporter
- Gateway Path:
  - Client -> Traefik(`websecure`) -> `gateway-standard-chain` + `sso-errors`/`sso-auth` -> target service; Grafana and Gatus routes use `gateway-standard-chain` only, and the Prometheus API route uses `prometheus-api-auth`
- Internal Path:
  - OTLP/log/trace traffic over `obs_net`

### Runtime and Deployment

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

## Interfaces

### Contracts

- Gateway path: Client -> Traefik(`websecure`) -> `gateway-standard-chain` + `sso-errors`/`sso-auth` -> target service; Grafana and Gatus routes use `gateway-standard-chain` only, and the Prometheus API route uses `prometheus-api-auth`.
- Internal path: OTLP/log/trace traffic over `obs_net`.

### Failure Boundaries

The data plane is kept over `obs_net` internal communication, and boot stability is improved through `service_healthy` dependency. The description records no failure boundary beyond the linked operations documents under Contracts.

## Decisions

### Decision Links

- **ADR**: [ADR-0021 Observability hardening and HA expansion](../decisions/0021-observability-hardening-and-ha-expansion-strategy.md)

### Quality and Risks

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

## Traceability

### Requirement Mapping

- **Requirement**: [REQ-0007 Observability](../../01.requirements/0007-observability.md)

### Currentness and Lineage

- **Tier Architecture Description**: [AD-0006 Observability Architecture Description](0006-observability-architecture.md)
- **Guide**: [Observability optimization hardening guide](../../05.operations/guides/07-observability/0044-observability-optimization-hardening.md)
- **Policy**: [Observability optimization hardening policy](../../05.operations/policies/07-observability/0044-observability-optimization-hardening.md)
- **Runbook**: [Observability optimization hardening runbook](../../05.operations/runbooks/07-observability/0044-observability-optimization-hardening.md)

#### Evolution

- Prometheus: scrape budget + remote_write tiering
- Loki: label cardinality budget + separate retention/compactor operation
- Tempo: per-service/endpoint sampling policy + span-burst protection
- Alloy: onboarding templating + modularized collection pipeline
