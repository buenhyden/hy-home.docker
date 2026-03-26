# ADR-0006: LGTM Stack and Grafana Alloy Selection

> Selection of Grafana LGTM Stack and Alloy for Unified Observability.

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 관측성 도구로 Grafana LGTM 스택(Loki, Grafana, Tempo, Mimir/Prometheus)과 Grafana Alloy 수집기를 선정한 배경과 이유를 기록한다.

## Context

현대적인 마이크로서비스 환경에서는 메트릭(Metrics), 로그(Logs), 트레이싱(Tracing)의 상관 분석(Correlation)이 필수적이다. 기존의 파편화된 도구들은 데이터 간의 연결 고리가 부족하여 장애 대응 시 맥락(Context)을 소실하는 문제가 있었다. 또한, 각 데이터 유형별로 서로 다른 에이전트(Promtail, Otel-Collector 등)를 관리해야 하는 운영 부담이 존재했다.

## Decision

- **Grafana LGTM Stack 채택**: 데이터 간의 자유로운 전환(Jump to logs from traces 등)을 지원하는 통합 에코시스템을 활용한다.
- **Grafana Alloy 채택**: OpenTelemetry(OTLP)와 Prometheus 생태계를 동시에 지원하며, 단일 바이너리로 다양한 텔레메트리 데이터를 수집/처리/라우팅하는 통합 에이전트를 사용한다.
- **S3 (MinIO) Backend**: Loki와 Tempo의 데이터를 클라우드 네이티브 방식인 S3(MinIO)에 저장하여 영속성과 확장성을 확보한다.

## Explicit Non-goals

- ELK(Elasticsearch, Logstash, Kibana) 스택의 전면 배제 (특수 목적의 전문 검색이 필요한 경우 개별 검토).
- 상용 SaaS(Datadog 등)로의 즉각적인 마이그레이션 지원.

## Consequences

- **Positive**:
    - **통합된 사용자 경험**: Grafana라는 단일 UI에서 모든 관측 데이터를 분석 가능.
    - **운영 단순화**: Alloy 하나로 모든 수집 기능을 대체하여 관리 포인트 감소.
    - **비용 효율성**: S3 기반 저장 방식을 통해 대용량 데이터 저장 비용 절감.
- **Trade-offs**:
    - **학습 곡선**: Grafana Alloy의 새로운 설정 언어(HCL-like)에 대한 숙련도 필요.
    - **추가 인프라**: MinIO 등의 백엔드 인프라 운영 부담.

## Alternatives

### Alternative 1: ELK Stack (Elasticsearch, Logstash, Kibana)

- **Good**: 강력한 전문 검색 기능, 정형 데이터 분석에 유리.
- **Bad**: 높은 메모리 및 스토리지 점유율, 트레이싱 연동이 상대적으로 부족함.

### Alternative 2: OpenTelemetry Collector (Vanilla)

- **Good**: 업계 표준이며 벤더 중립적임.
- **Bad**: Grafana 생태계(Loki/Prometheus 등)와의 밀접한 연동 기능(Discovery 등)이 Alloy에 비해 부족함.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-06-observability.md]`
- **ARD**: `[../02.ard/0006-observability-architecture.md]`
- **Spec**: `[../04.specs/06-observability/spec.md]`
