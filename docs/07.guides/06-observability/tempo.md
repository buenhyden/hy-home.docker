# Tempo System Guide

> Distributed tracing and trace-to-metrics correlation.

---

## Overview (KR)

이 문서는 Tempo에 대한 가이드다. Tempo는 분산 추적(Distributed Tracing) 데이터를 수집, 저장, 쿼리하는 시스템으로, 마이크로서비스 환경에서 요청의 흐름과 지연 시간(Latency)을 시각화한다. 특히 Span Metrics와 Service Graphs를 자동으로 생성하여 서비스 간의 의존성 지도를 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Backend Developer
- SRE / DevOps
- Architect

## Purpose

분산 추적의 기본 개념을 이해하고, TraceQL을 사용하여 성능 병목을 추적하며, 메트릭 및 로그와 연동하여 장애 원인을 파악하는 방법을 익힌다.

## Prerequisites

- [Grafana Alloy](alloy.md) OTLP 수집 설정 완료
- [MinIO](../../../infra/04-data/lake-and-object/minio/README.md) `tempo-bucket` 생성을 통한 스토리지 확보
- [Grafana](grafana.md) Tempo 및 Prometheus 데이터 소스 연결

## Step-by-step Instructions

### 1. 분산 추적 데이터 조회 (TraceQL)

Grafana의 `Explore` 메뉴에서 `Tempo` 데이터 소스를 선택한다. `TraceQL` 쿼리 언어를 사용하여 특정 조건의 트레이스를 검색할 수 있다.

- 예: `{ duration > 100ms && resource.service.name = "api-gateway" }`

### 2. Trace-to-Metrics Correlation

Tempo는 수집된 트레이스를 기반으로 메트릭(Span Metrics)을 생성하여 Prometheus로 전송한다. 트레이스 상세 뷰에서 관련 메트릭 대시보드로 바로 이동할 수 있다.

### 3. Service Graphs 및 Dependency Map

`Metrics Generator`가 활성화된 경우, 서비스 간의 호출 관계와 에러율, 지연 시간을 시각화한 서비스 그래프를 확인할 수 있다.

### 4. 로그와 연동 (Trace ID Correlation)

Loki 로그와 연동되어 있는 경우, 특정 로그 라인에 포함된 Trace ID를 클릭하여 해당 요청의 전체 트레이스 뷰로 전환할 수 있다.

## Common Pitfalls

- **Instrumentation 누락**: 트레이스 전파(Propagation)가 끊기면 전체 요청 흐름을 볼 수 없다. 공통 라이브러리나 미들웨어에서 Context 전달을 확인하라.
- **WAL 관리**: 로컬 디스크의 WAL(Write-Ahead Log) 공간이 부족하면 트레이스 저장이 중단된다.
- **MinIO 연결**: Tempo와 MinIO 간의 네트워크 지연이나 설정 오류는 트레이스 조회를 불가능하게 만든다.

## Related Documents

- **Infrastructure**: `[infra/06-observability/tempo/README.md](../../../infra/06-observability/tempo/README.md)`
- **Operation**: `[../08.operations/06-observability/tempo.md](../../08.operations/06-observability/tempo.md)`
- **Runbook**: `[../09.runbooks/06-observability/tempo.md](../../09.runbooks/06-observability/tempo.md)`
