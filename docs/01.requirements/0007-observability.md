---
title: "Observability Tier Requirements"
version: "2.0.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "requirements"
artifact_id: "REQ-0007"
created: "2026-03-26"
---

# Observability Tier Requirements

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the requirement payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

##### Problem and Outcome

When metrics, logs and traces are fragmented, finding the root cause of a
failure takes longer and availability suffers. The observability tier
(`06-observability`) gives one view of every infrastructure and application
service by integrating Prometheus, Loki, Tempo and Grafana with Grafana Alloy,
Alertmanager, Pushgateway, cAdvisor, node and GPU exporters, Pyroscope, Gatus
and Dozzle.

##### Stakeholders

- **DevOps/SRE**: watches availability and resource use of every container on
  one dashboard and is alerted when a threshold is exceeded.
- **Application developer**: checks error logs after a deployment and
  correlates a transaction's trace with its logs by request ID.

The owner, @buenhyden, writes, reviews and accepts this package.

#### Scope

##### In Scope

- Metrics, logs, traces and profiles collection, dashboards and
  their provisioning, alert routing, and service status checks.

##### Constraints and Exclusions

- **Out of Scope**: Ongoing analysis of business logs, and external cloud
  monitoring services.
- **Agent boundary**: An agent may run metric queries and check dashboard and
  alert status. It must not delete observability data or disable an alert
  policy without approval.

**Assumptions.**

Every monitored service exposes metrics, logs or traces in a form the unified
collector or the metrics server can read.

**Risks.**

- Log and trace storage depends on the object storage in `04-data`; a data
  tier failure interrupts persistence.
- Dashboard login depends on the identity provider in `02-auth`.

#### Requirements

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0007-FR-0001 | Collect and store time-series metrics from every monitored service. | Fragmented metrics, logs and traces slow root-cause analysis; DevOps and SRE watch availability and resource use of every container on one dashboard. | Every target declared in the current scrape configuration renders without omission; runtime verification confirms the expected targets are up. | must |
| REQ-0007-FR-0002 | Aggregate logs from distributed services centrally and persist them to object storage. | Fragmented logs slow root-cause analysis; an application developer checks error logs after a deployment. | Log storage is configured against the object storage bucket scoped to logs. | must |
| REQ-0007-FR-0003 | Collect distributed traces between services and persist them to object storage. | An application developer correlates a transaction's trace with its logs by request ID. | Trace storage is configured against the object storage bucket scoped to traces. | must |
| REQ-0007-FR-0004 | Use one unified collector to receive and forward OTLP telemetry. | The tier gives one view of every service by integrating its backends with Grafana Alloy. | The collector declares OTLP receivers and forwards to the log, trace and metric backends. | must |
| REQ-0007-FR-0005 | Control dashboard access through the platform's OIDC identity provider. | This package records no rationale for this requirement. | Dashboard login goes only through the identity provider; the local login form and local sign-up are disabled. | must |
| REQ-0007-FR-0006 | Route alerts to a team notification channel. | DevOps and SRE are alerted when a threshold is exceeded. | Chat notification receivers and their secrets render; email delivery is not configured yet, and delivery within 60 seconds is claimed only with separate runtime rehearsal evidence. | must |

##### Functional Requirements

- **REQ-0007-FR-0001**: Collect and store time-series metrics from every monitored service.
- **REQ-0007-FR-0002**: Aggregate logs from distributed services centrally and persist them to object storage.
- **REQ-0007-FR-0003**: Collect distributed traces between services and persist them to object storage.
- **REQ-0007-FR-0004**: Use one unified collector to receive and forward OTLP telemetry.
- **REQ-0007-FR-0005**: Control dashboard access through the platform's OIDC identity provider.
- **REQ-0007-FR-0006**: Route alerts to a team notification channel.

##### Quality Requirements

This package declares no quality requirement and records no reason why none applies.

#### Traceability

##### Sources

This package records the owner's requirements for the observability tier; no upstream
document governs it.

##### Verification Links

###### Acceptance Conditions
<!-- core-payload-level:4 -->

- **REQ-0007-FR-0001**: Every target declared in the current scrape
  configuration renders without omission; runtime verification confirms the
  expected targets are up.
- **REQ-0007-FR-0002**: Log storage is configured against the object storage
  bucket scoped to logs.
- **REQ-0007-FR-0003**: Trace storage is configured against the object storage
  bucket scoped to traces.
- **REQ-0007-FR-0004**: The collector declares OTLP receivers and forwards to
  the log, trace and metric backends.
- **REQ-0007-FR-0005**: Dashboard login goes only through the identity
  provider; the local login form and local sign-up are disabled.
- **REQ-0007-FR-0006**: Chat notification receivers and their secrets
  render; email delivery is not configured yet. Delivery within 60 seconds is claimed only with separate
  runtime rehearsal evidence.

###### Verification Method
<!-- core-payload-level:4 -->

Each condition is judged by reviewing the rendered configuration for the scrape, storage, collector, login and alert settings, while target availability and the 60-second alert delivery are judged by a runtime observation. No current Spec Package cites REQ-0007; a Spec that implements it records the evidence in its Task. The evidence is the review result and the observed timings, recorded in that Task. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

###### Downstream Links
<!-- core-payload-level:4 -->

- **Architecture Description**: [Observability architecture](../02.architecture/01.descriptions/0006-observability-architecture.md)
- **ADR**: [ADR-0053 Observability Object Storage on SeaweedFS](../02.architecture/02.decisions/0053-observability-storage-on-seaweedfs.md)
- **Retired domain Spec SPEC-0007** (observability): replaced by the observability guides, policies and runbooks in the operations catalog under `docs/05.operations/`.
- **Retired requirement REQ-0018** (observability optimization hardening): retired under SPEC-0169 because every clause named an implementation artifact (a middleware chain, run account, secret mount, compose declaration, or CI gate) rather than a solution-independent need. Its implementation contract lives in the observability operations catalog policy under `docs/05.operations/`, and its documentation traceability clause moved to REQ-0026-FR-0011.

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
