# Observability Architecture Reference Document

> Integrated Telemetry Pipeline with LGTM Stack and Grafana Alloy.

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 관측성(Observability) 계층인 `06-observability`의 참조 아키텍처를 정의한다. 로컬 환경에서 클라우드 수준의 관측성을 확보하기 위해 LGTM 스택(Loki, Grafana, Tempo, Mimir/Prometheus)을 Grafana Alloy 및 Pyroscope와 통합하여 구축한다.

## Summary

Observability 티어는 시스템 전반의 상태 정보를 수집, 저장, 시각화하며, 장애 시 상관 분석(Correlation Analysis)을 통해 문제 해결을 가속화한다. 모든 데이터는 OTLP(OpenTelemetry Protocol)를 준수하며, MinIO 기반의 S3 백엔드 스토리지를 활용하여 영속성을 보장한다.

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
  - 메트릭: Prometheus Local TSDB (7일 보관)
  - 로그/트레이스: MinIO S3 Buckets (15일~30일 보관 정책)
- **Data Boundaries**: 모든 텔레메트리 데이터는 `infra_net` 내부망에서만 소통함을 원칙으로 한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose v2.x 기반 컨테이너 오케스트레이션.
- **Deployment Model**: `obs` 프로파일을 통해 선택적으로 로드되는 시스템 인프라.
- **Operational Evidence**: Grafana Provisioning API를 통한 코드 기반의 대시보드 관리.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-06-observability.md]`
- **Spec**: `[../04.specs/06-observability/spec.md]`
- **ADR**: `[../03.adr/0006-lgtm-stack-selection.md]`
- **Plan**: `[../05.plans/2026-03-26-06-observability-standardization.md]`
