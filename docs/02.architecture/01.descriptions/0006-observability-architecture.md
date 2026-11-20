---
title: "Observability Architecture Description"
version: "2.0.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "AD-0006"
parent_ids:
- "REQ-0007"
created: "2026-03-26"
---

# Observability Architecture Description

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-description payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context and Boundaries

##### System Boundary

- **Owns:** centralized logs (Loki), metrics and alerting (Prometheus,
  Alertmanager), traces (Tempo), profiles (Pyroscope), dashboards (Grafana),
  telemetry collection (Alloy), availability checks (Gatus), and optional
  Docker-log inspection (Dozzle, a separate leaf).
- **Consumes:** SeaweedFS (`04-data`) S3 storage for logs and traces;
  Keycloak (`02-auth`) OIDC for Grafana, Gatus and Dozzle; `mng-pg` for
  Grafana state. Gatus keeps a local SQLite store.
- **Does not own:** application security logs (`03-security`) or business
  statistics.
- **Non-goals:** dependence on external cloud monitoring vendors.

###### Purpose and Readers
<!-- core-payload-level:4 -->

`06-observability` collects, stores and shows platform telemetry so incidents
can be correlated across logs, metrics, traces and profiles. It runs Loki,
Grafana, Tempo and Prometheus with Grafana Alloy, Alertmanager, Pushgateway,
cAdvisor, node-exporter, Gatus, Pyroscope and a DCGM GPU exporter,
fully self-hosted.

###### Context
<!-- core-payload-level:4 -->

Alloy collects Docker logs, OTLP traces and pprof targets; Prometheus scrapes exporters and services; Traefik sends traces straight to Tempo; k6 sends OTLP to an authenticated Alloy receiver. Loki and Tempo store objects in SeaweedFS (`04-data`), and Grafana, Gatus and Dozzle use Keycloak OIDC (`02-auth`).

##### Constraints

The stack is fully self-hosted with no dependence on external cloud monitoring vendors. Prometheus keeps a local TSDB as the durable authority, and approved Kubernetes LAN ingress and query exceptions stay under POL-0096.

#### Structure

##### Building Blocks

All core services are in `infra/06-observability/docker-compose.yml`; Dozzle
is in `infra/06-observability/dozzle/docker-compose.yml`. Alloy discovers
Docker logs and forwards them to Loki, receives OTLP traces and forwards them
to Tempo, and declares pprof scrape targets for Pyroscope. Prometheus scrapes
exporters, services and Alloy self-metrics directly. Grafana queries each
datasource. Traefik sends its own traces straight to Tempo.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Docker log collection | The description names no producer for this interface. | Alloy, forwarding to Loki | The description links no contract for this interface. | The description records no failure handling for this interface. |
| OTLP trace receiver | Applications | Alloy, forwarding to Tempo | OTLP | The description records no failure handling for this interface. |
| Traefik traces | Traefik | Tempo | The description links no contract for this interface. | The description records no failure handling for this interface. |
| Authenticated Alloy quality-metrics receiver | k6 | Alloy, forwarding by Prometheus remote write | `config.home.alloy` | The description records no failure handling for this interface. |
| Prometheus scrapes on `obs_net` | cAdvisor, exporters, services and Alloy self-metrics | Prometheus | The description links no contract for this interface. | The description records no failure handling for this interface. |
| pprof scrape targets | Declared Alloy pprof targets | Pyroscope | The description links no contract for this interface. | The description records no failure handling for this interface. |
| S3 object storage on `object_net` | SeaweedFS (`04-data`) | Loki (`loki-bucket`) and Tempo (`tempo-bucket`) | [ADR-0053 Observability object storage on SeaweedFS](../02.decisions/0053-observability-storage-on-seaweedfs.md) | Bucket history is excluded from HOME Restic state; lost history is outside backup recovery and services collect new data. |
| Keycloak OIDC | Keycloak (`02-auth`) | Grafana, Gatus and Dozzle | OIDC | The description records no failure handling for this interface. |
| Grafana state store | `mng-pg` (`04-data`) | Grafana | The description links no contract for this interface. | The description records no failure handling for this interface. |
| Prometheus API route | Prometheus | The description names no consumer for this interface. | `prometheus-api-auth@file` | The description records no failure handling for this interface. |

Scrapes and datasource queries use `obs_net`, object storage uses `object_net`, and UI routes use `edge_net`. The Alloy receiver is authenticated; the Prometheus API route uses `prometheus-api-auth@file`.

#### Runtime Behavior

##### Normal Flow

###### Runtime View
<!-- core-payload-level:4 -->

- **Metrics:** cAdvisor, exporters and services -> Prometheus; Alloy
  self-metrics -> Prometheus scrape.
- **Logs:** Docker logs -> Alloy -> Loki -> SeaweedFS `loki-bucket`
  (`retention_period: 168h`).
- **Traces:** application OTLP -> Alloy -> Tempo -> SeaweedFS `tempo-bucket`.
- **Quality metrics:** k6 OTLP -> authenticated Alloy receiver
  (`config.home.alloy`) -> Prometheus remote write. A 2026-10-08 HOME canary
  passed for the named inputs (SPEC-0214, since deleted); that dated result
  does not certify later source or real application load.
- **Profiles:** declared Alloy pprof targets -> Pyroscope (local filesystem
  backend); collection success is not verified.

Prometheus keeps a local TSDB. Scrapes and datasource queries use `obs_net`,
object storage `object_net`, UI routes `edge_net`. Approved Kubernetes LAN
ingress and query exceptions stay under POL-0096.

###### Deployment View
<!-- core-payload-level:4 -->

`obs` selects the full set; `obs-core` (Prometheus, Grafana), `obs-host`
(node-exporter, cAdvisor), `logs`, `tracing`, `profiling`, `alerting`,
`availability` (Gatus) and `batch-metrics` (Pushgateway) select narrower sets.
`dev` selects Prometheus, Grafana, node-exporter, cAdvisor and Gatus.
`obs-gpu` alone selects `dcgm-exporter`. Dozzle is selected by `admin` or
`admin-logs`. Prometheus, Grafana, Loki, Alloy, Tempo, Pyroscope,
node-exporter, cAdvisor, Gatus, Alertmanager and `dcgm-exporter` are HOME;
Pushgateway is OPTIONAL. Starting a HOME profile does not stop an already
running optional container.

##### Failure and Recovery

The HOME Restic state set excludes SeaweedFS `loki-bucket` and `tempo-bucket`
volume files. Lost object history is outside HOME backup recovery, and the
services collect new data. The [backup policy](../../05.operations/02.policies/10.platform-and-backup/0021-backup-and-restore.md)
owns the recovery boundary. The open Tempo retention gap is recorded below.

#### Quality Scenarios

##### Scenarios

###### Quality Attributes
<!-- core-payload-level:4 -->

- **Performance:** Alloy batches traces before export.
- **Security:** Grafana, Gatus and Dozzle use native Keycloak OIDC; the other
  UIs use ForwardAuth; the Prometheus API route uses `prometheus-api-auth@file`.
- **Reliability:** the current snapshot boundary for Loki and Tempo is stated
  under Failure and Recovery. SeaweedFS use alone provides no evidence of recovery
  for the excluded telemetry history.
- **Scalability:** the Prometheus local TSDB is the durable authority; the
  enabled remote-write receiver does not imply an external long-term store.
- **Observability:** the stack includes self-monitoring dashboards.

###### Risks
<!-- core-payload-level:4 -->

The Tempo policy targets 24h retention, but `tempo/config/tempo.yaml` sets no
`block_retention`, so the version default (336h) applies. This gap is open.

##### Trade-offs

- The stack is fully self-hosted with no dependence on external cloud
  monitoring vendors (Constraints).
- Prometheus keeps a local TSDB as the durable authority; the enabled
  remote-write receiver does not imply an external long-term store, and a
  long-term metrics store needs a Stage 03 change (Quality Attributes,
  Evolution).
- The HOME Restic state set excludes SeaweedFS `loki-bucket` and
  `tempo-bucket` volume files; the accepted cost is that lost object history is
  outside HOME backup recovery and the services collect new data (Failure and
  Recovery).
- The Tempo retention gap (policy 24h, version default 336h) is open (Risks).

#### Decisions and Adoption

##### Decisions

- [ADR-0053 Observability object storage on SeaweedFS](../02.decisions/0053-observability-storage-on-seaweedfs.md)

##### Adoption Boundaries

###### Requirement Mapping
<!-- core-payload-level:4 -->

- [REQ-0007 Observability requirements](../../01.requirements/0007-observability.md)

###### Currentness and Lineage
<!-- core-payload-level:4 -->

- [Derived Compose image projection](../../../infra/tech-stack.versions.json)

###### Evolution
<!-- core-payload-level:4 -->

A long-term metrics store or a Tempo retention setting needs a Stage 03
change.

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
