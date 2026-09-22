---
title: "Observability Architecture Description"
version: "1.0.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "AD-0006"
parent_ids:
- "REQ-0007"
created: "2026-03-26"
---
# Observability Architecture Description

> Integrated Telemetry Pipeline with LGTM Stack and Grafana Alloy.

## Context and Stakeholders

이 문서는 `hy-home.docker` 플랫폼의 관측성(Observability) 계층인 `06-observability`의 참조 아키텍처를 정의한다. 로컬 환경에서 클라우드 수준의 관측성을 확보하기 위해 현재 구현된 LGTM 스택(Loki, Grafana, Tempo, Prometheus)을 Grafana Alloy, Alertmanager, Pushgateway, cAdvisor, Pyroscope와 통합하여 구축한다.

### Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

Observability 티어는 시스템 전반의 상태 정보를 수집, 저장, 시각화하며, 장애 시 상관 분석(Correlation Analysis)을 통해 문제 해결을 가속화한다. 현재 compose는 OTLP trace ingress, Docker log discovery, Prometheus scrape/remote-write 경로를 제공하고, Loki/Tempo는 SeaweedFS 기반 S3 백엔드 스토리지를 사용한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - 중앙 집중형 로깅 (Loki)
  - 시계열 메트릭 수집 및 알람 (Prometheus/Alertmanager)
  - 분산 트레이싱 (Tempo)
  - 지속적 프로파일링 (Pyroscope)
  - 통합 대시보드 (Grafana)
  - 통합 텔레메트리 수집 (Alloy)
- **Consumes**:
  - **SeaweedFS (04-data)**: 로그 및 트레이스 데이터 저장을 위한 S3 스토리지.
  - **Keycloak (02-auth)**: Grafana SSO 로그인을 위한 OIDC 공급자.
- **Does Not Own**:
  - 애플리케이션 보안 로그 (03-security 소관)
  - 비즈니스 통계 데이터 (Data Warehouse 소관)
- **Non-goals**:
  - 외부 클라우드 모니터링 벤더에 대한 종속성 (완전한 Self-hosted 지향)

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: Alloy를 통한 비동기 데이터 처리를 통해 애플리케이션 오버헤드 최소화.
- **Security**: Keycloak OIDC 기반의 역할 기반 권한 제어(RBAC) 적용.
- **Reliability**: Loki/Tempo의 SeaweedFS object blocks와 각 서비스의 local WAL/working state를 함께 다루는 복구 경계.
- **Scalability**: Prometheus는 현재 local TSDB가 durable authority이며 remote-write receiver 활성화만으로 외부 장기 저장소를 의미하지 않는다.
- **Observability**: 자기 자신에 대한 모니터링(Self-monitoring) 대시보드 포함.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

현재 source에서 Docker logs와 OTLP traces는 **Grafana Alloy**를 거쳐
Loki/Tempo로 이동하고, Prometheus는 exporters/services를 직접 scrape한다.
Alloy self-metrics만 remote-write로 Prometheus에 전달된다. Pyroscope write
sink는 있으나 profile source가 없으므로 end-to-end profile collection은
현재 구성만으로 성립하지 않는다. 사용자는 **Grafana**에서 각 datasource를
조회한다.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**:
  - **Metrics Flow**: cAdvisor/Exporters/Services -> Prometheus; Alloy self-metrics -> Prometheus remote write
  - **Logs Flow**: Docker Logs -> Alloy -> Loki -> SeaweedFS
  - **Traces Flow**: App (OTLP) -> Alloy -> Tempo -> SeaweedFS
  - **Profiles Flow**: Pyroscope sink is configured, but no Alloy profile source is declared
- **Storage Strategy**:
  - 메트릭: Prometheus local TSDB
  - 로그: Loki SeaweedFS bucket `loki-bucket`, `retention_period: 168h`
  - 트레이스: Tempo SeaweedFS bucket `tempo-bucket`, `block_retention: 24h`
  - 프로파일: Pyroscope local filesystem backend
- **Data Boundaries**: 모든 텔레메트리 데이터는 `infra_net` 내부망에서만 소통함을 원칙으로 한다.

## Deployment View

- **Runtime / Platform**: Docker Compose v2.x 기반 컨테이너 오케스트레이션.
- **Deployment Model**: `prometheus`, `grafana`, `loki`, `alloy`,
  `node-exporter`, `cadvisor`, `gatus`, `alertmanager`는 `HOME`.
  `tempo`, `pyroscope`, `pushgateway`는 `OPTIONAL`. `obs`는 전체
  compatibility profile이며 `obs-core`, `obs-host`, `logs`, `tracing`,
  `profiling`, `alerting`, `availability`, `batch-metrics`가 narrower
  activation을 제공한다. HOME profile start는 이미 실행 중인 optional
  container를 자동 중지하지 않는다.
- **Operational Evidence**: Grafana provisioning files, root compose profile validation, service-local compose validation with root network/secret context, and hardening script output.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Spec**: [../../03.specs/007-observability/spec.md](0006-observability-architecture.md)
- **ADR**: [../decisions/0006-lgtm-stack-selection.md](../decisions/0006-lgtm-stack-selection.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
