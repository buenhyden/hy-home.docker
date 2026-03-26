# ADR-0015: Specialized Analytics Engines Selection

> This Architecture Decision Record (ADR) formalizes the selection of specialized analytics engines over a unified "one-size-fits-all" database approach for the `hy-home.docker` platform.

---

## Overview (KR)

이 문서는 `04-data/analytics` 티어에서 InfluxDB, ksqlDB, OpenSearch, StarRocks를 개별 분석 엔진으로 채택한 배경과 결정 사항을 기록한다. 대규모 시계열, 스트림, 로그, OLAP 데이터를 단일 범용 DB에서 처리할 때의 한계를 극복하고 각 도메인별 최적의 성능을 보장하기 위한 전략이다.

## Context

`hy-home.docker` 플랫폼은 스마트 홈 센서의 고밀도 시계열 데이터, 실시간 이벤트 스트림, 마이크로서비스의 대규모 로그, 그리고 복잡한 OLAP 분석 요구사항을 동시에 수용해야 한다. 기존 PostgreSQL만으로는 다음과 같은 한계가 발생한다:

- **Write Throughput**: 수천 개의 센서 메트릭 기록 시 동시성 제어 오버헤드.
- **Query Performance**: 수억 건의 로그 검색 및 조인 연산 시의 지연 시간.
- **Problem Storage Efficiency**: 비압축 데이터의 기하급수적 증가로 인한 스토리지 비용.

따라서 각 데이터 모델에 특화된 전용 엔진을 도입하여 워크로드를 분산시키기로 결정하였다.

## Decision

- **TSDB**: InfluxDB 2.x 채택 (고밀도 시계열 데이터 압축 및 보관 최적화).
- **Stream Processing**: ksqlDB 채택 (Kafka Topic에 대한 SQL 기반 실시간 처리 및 변환).
- **Log Engine**: OpenSearch 2.x 채택 (분산 루씬 기반 고속 전문 검색 및 시각화).
- **OLAP Warehouse**: StarRocks 3.x 채택 (MPP 기반 실시간 조인 및 고속 데이터웨어하우스 구축).

## Explicit Non-goals

- 핵심 트랜잭션 데이터(사용자 정보, 시스템 설정 등)를 분석 엔진에 직접 저장하는 행위는 지양한다 (원본은 PostgreSQL에 유지).
- 각 엔진 간의 중복된 데이터 저장 최소화.

## Consequences

- **Positive**:
  - 각 도메인별 극대화된 조회 및 기록 성능 확보.
  - 데이터 생애 주기(Retention Policy)의 개별 제어 가능.
  - 분석 부하와 서비스 부하의 물리적 격리.
- **Trade-offs**:
  - 운영 복잡성 증가 (엔진별 모니터링 및 백업 관리 필요).
  - 인프라 리소스(CPU/RAM) 추가 요구량 증가.
  - 엔진 간 데이터 동기화(CDC/Stream) 로직 구축 오버헤드.

## Alternatives

### Alternative 01: PostgreSQL 확장 (TimescaleDB, pg_search 등 사용)

- **Good**: 익숙한 SQL 문법, 운영 단일화.
- **Bad**: 극한의 스케일아웃 상황에서의 성능 한계, 스트림 처리 엔진의 부재.

### Alternative 02: 클라우드 기반 관리 서비스 (BigQuery, Redshift 등)

- **Good**: 운영 오버헤드 제로, 무한 확장성.
- **Bad**: 로컬 도커 환경 구축 불가, 데이터 주권 및 보안 우려.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../02.ard/0012-data-analytics-architecture.md)
- **Spec**: [spec.md](../04.specs/04-data-analytics/spec.md)
- **Guide**: [README.md](../07.guides/04-data/analytics/README.md)
