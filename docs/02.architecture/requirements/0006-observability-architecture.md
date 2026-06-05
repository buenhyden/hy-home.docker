---
status: active
---

<!-- Target: docs/02.architecture/requirements/0006-observability-architecture.md -->

# Observability Architecture Reference Document (ARD)

> Integrated Telemetry Pipeline with LGTM Stack and Grafana Alloy.

## Overview

이 문서는 `hy-home.docker` 플랫폼의 관측성(Observability) 계층인 `06-observability`의 참조 아키텍처를 정의한다. 로컬 환경에서 클라우드 수준의 관측성을 확보하기 위해 현재 구현된 LGTM 스택(Loki, Grafana, Tempo, Prometheus)을 Grafana Alloy, Alertmanager, Pushgateway, cAdvisor, Pyroscope와 통합하여 구축한다.

## Summary

Observability 티어는 시스템 전반의 상태 정보를 수집, 저장, 시각화하며, 장애 시 상관 분석(Correlation Analysis)을 통해 문제 해결을 가속화한다. 현재 compose는 OTLP trace ingress, Docker log discovery, Prometheus scrape/remote-write 경로를 제공하고, Loki/Tempo는 MinIO 기반 S3 백엔드 스토리지를 사용한다.

## Boundaries & Non-goals

- **Owns**:
  - 중앙 집중형 로깅 (Loki)
  - 시계열 메트릭 수집 및 알람 (Prometheus/Alertmanager)
  - 분산 트레이싱 (Tempo)
  - 지속적 프로파일링 (Pyroscope)
  - 통합 대시보드 (Grafana)
  - 통합 텔레메트리 수집 (Alloy)
- **Consumes**:
  - **MinIO (04-data)**: 로그 및 트레이스 데이터 저장을 위한 S3 스토리지.
  - **Keycloak (02-auth)**: Grafana SSO 로그인을 위한 OIDC 공급자.
- **Does Not Own**:
  - 애플리케이션 보안 로그 (03-security 소관)
  - 비즈니스 통계 데이터 (Data Warehouse 소관)
- **Non-goals**:
  - 외부 클라우드 모니터링 벤더에 대한 종속성 (완전한 Self-hosted 지향)

## Quality Attributes

- **Performance**: Alloy를 통한 비동기 데이터 처리를 통해 애플리케이션 오버헤드 최소화.
- **Security**: Keycloak OIDC 기반의 역할 기반 권한 제어(RBAC) 적용.
- **Reliability**: Loki/Tempo의 S3 백엔드 구성을 통해 노드 장애 시에도 데이터 보존.
- **Scalability**: Prometheus의 Remote Write와 S3 스토리지를 통한 수평적 확장 대비.
- **Observability**: 자기 자신에 대한 모니터링(Self-monitoring) 대시보드 포함.

## System Overview & Context

모든 인프라 컨테이너 및 애플리케이션은 **Grafana Alloy**로 텔레메트리 데이터를 전송한다. Alloy는 데이터를 정제하여 각 목적지(Prometheus, Loki, Tempo, Pyroscope)로 라우팅하며, 사용자는 **Grafana**의 통합 대시보드를 통해 이를 소비한다.

## Data Architecture

- **Key Entities / Flows**:
  - **Metrics Flow**: cAdvisor/Exporters -> Alloy -> Prometheus
  - **Logs Flow**: Docker Logs -> Alloy -> Loki -> MinIO
  - **Traces Flow**: App (OTLP) -> Alloy -> Tempo -> MinIO
  - **Profiles Flow**: App -> Alloy -> Pyroscope
- **Storage Strategy**:
  - 메트릭: Prometheus local TSDB
  - 로그: Loki MinIO bucket `loki-bucket`, `retention_period: 168h`
  - 트레이스: Tempo MinIO bucket `tempo-bucket`, `block_retention: 24h`
  - 프로파일: Pyroscope local filesystem backend
- **Data Boundaries**: 모든 텔레메트리 데이터는 `infra_net` 내부망에서만 소통함을 원칙으로 한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose v2.x 기반 컨테이너 오케스트레이션.
- **Deployment Model**: `obs` 프로파일을 통해 선택적으로 로드되는 시스템 인프라.
- **Operational Evidence**: Grafana provisioning files, root compose profile validation, service-local compose validation with root network/secret context, and hardening script output.

## Related Documents

- **PRD**: [../../01.requirements/2026-03-26-06-observability.md](../../01.requirements/2026-03-26-06-observability.md)
- **Spec**: [../../03.specs/06-observability/spec.md](../../03.specs/06-observability/spec.md)
- **ADR**: [../decisions/0006-lgtm-stack-selection.md](../decisions/0006-lgtm-stack-selection.md)
- **Plan**: [../../04.execution/plans/2026-03-26-06-observability-standardization.md](../../04.execution/plans/2026-03-26-06-observability-standardization.md)
