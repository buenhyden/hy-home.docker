# Observability Tier Product Requirements

> Centralized telemetry, monitoring, and debugging hub.

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 관측성(Observability) 계층인 `06-observability`의 제품 요구사항을 정의한다. LGTM 스택(Loki, Grafana, Tempo, Mimir/Prometheus)과 Grafana Alloy를 통합하여 시스템 전반의 상태를 실시간으로 모니터링하고 가시화하는 것을 목표로 한다.

## Vision

제공되는 모든 인프라 및 애플리케이션 서비스의 상태를 단일 지점(Single Source of Truth)에서 파악하고, 장애 발생 시 원인을 즉각적으로 규명할 수 있는 고도화된 관측 환경을 구축한다.

## Problem Statement

마이크로서비스 아키텍처에서 서비스 간 연동이 복잡해짐에 따라, 로그만으로는 장애의 근본 원인을 파악하기 어렵다. 메트릭, 로그, 트레이싱이 파편화되어 있으면 문제 해결 시간이 길어지며 시스템 가용성이 저하된다.

## Personas

- **Persona 1: DevOps/SRE**: 전체 인프라의 가용성과 성능을 상시 모니터링하고 임계값 초과 시 알람을 수신한다.
- **Persona 2: Application Developer**: 신규 기능 배포 후 오류 로그를 확인하고 분산 트레이싱을 통해 지연 구간을 최적화한다.

## Key Use Cases

- **STORY-01**: 운영자는 Grafana 대시보드에서 모든 컨테이너의 CPU/Memory 사용량을 한눈에 확인한다.
- **STORY-02**: 개발자는 요청 ID를 통해 특정 트랜잭션의 트레이스(Trace)와 관련 로그(Log)를 상관 분석한다.
- **STORY-03**: 시스템 장애 시 Alertmanager가 Slack/Email로 알람을 전송하여 즉각 대응하게 한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: Prometheus를 통해 실시간 시계열 메트릭을 수집하고 저장해야 한다.
- **REQ-PRD-FUN-02**: Loki를 통해 분산 노드의 로그를 중앙으로 집계하고 S3(MinIO)에 영구 보관해야 한다.
- **REQ-PRD-FUN-03**: Tempo를 통해 서비스 간 분산 트레이싱 정보를 수집해야 한다.
- **REQ-PRD-FUN-04**: Grafana Alloy를 단일 수집기(Unified Collector)로 사용하여 OTLP 데이터를 처리해야 한다.
- **REQ-PRD-FUN-05**: Keycloak OIDC 연동을 통해 Grafana 대시보드 접근 권한을 관리해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: 모든 인프라 서비스의 메트릭 수집율 100% 달성.
- **REQ-PRD-MET-02**: 장애 발생 시 알람 도달 시간 60초 이내 확보.

## Scope and Non-goals

- **In Scope**:
    - LGTM Stack (Loki, Grafana, Tempo, Prometheus) 구성
    - Grafana Alloy 및 Pyroscope 통합
    - Alertmanager 연동 및 대시보드 자동 프로비저닝
- **Out of Scope**:
    - 비즈니스 로그의 상시 분석 및 통계 (ELK Stack 영역)
    - 외부 클라우드 모니터링 서비스와의 연동

## Risks, Dependencies, and Assumptions

- **Persistence Layer**: Loki와 Tempo가 MinIO(`04-data`)에 의존하므로 데이터 계층 장애 시 관측 데이터 저장이 중단될 수 있다.
- **Auth Layer**: Grafana 로그인 및 권한 관리가 Keycloak(`02-auth`)에 의존한다.

## AI Agent Requirements

- **Allowed Actions**: Prometheus 쿼리(PromQL) 실행, 대시보드 상태 조회, 알람 상태 확인.
- **Disallowed Actions**: 운영 데이터 임의 삭제, 알람 정책 임의 해제.

## Related Documents

- **ARD**: `[../02.ard/0006-observability-architecture.md]`
- **Spec**: `[../04.specs/06-observability/spec.md]`
- **ADR**: `[../03.adr/0006-lgtm-stack-selection.md]`
