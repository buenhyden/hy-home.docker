# PRD: Analytics Tier (04-data/analytics)

> This document defines the product requirements for the specialized analytics data engines within the `04-data/analytics` sub-tier.

---

## [Analytics Tier] Product Requirements

## Overview (KR)

본 문서는 `04-data/analytics` 서브 티어의 전문화된 데이터 분석 엔진들(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 제품 요구사항을 정의한다. 시계열 데이터, 스트림 처리, 로그 검색, 그리고 대규모 OLAP 분석 환경을 통합적으로 구축하여 플랫폼의 데이터 인사이트 추출 능력을 극대화하는 것을 목표로 한다.

## Vision

플랫폼에서 발생하는 모든 정형/비정형 데이터를 실시간으로 수집, 가공, 분석하여 사용자에게 즉각적이고 심층적인 시각화 및 인사이트를 제공하는 고성능 분석 허브를 구축한다.

## Problem Statement

현재 핵심 데이터(SQL, KV)와 분석용 데이터가 분리되지 않거나, 시계열 및 로그 데이터 처리를 위한 전용 엔진이 부재하여 대규모 데이터 분석 시 성능 저하 및 운영 복잡도가 발생하고 있다.

## Personas

- **Data Scientist**: 정교한 쿼리와 OLAP 분석을 통해 트렌드를 도출해야 함.
- **SRE/DevOps**: 실시간 로그 검색 및 시스템 메트릭 모니터링이 필요함.
- **Home Automation User**: 실시간 차트와 센서 데이터의 변화를 지연 없이 확인하고 싶어함.

## Key Use Cases

- **STORY-01**: 사용자는 대시보드를 통해 지난 1년간의 스마트 홈 센서 데이터 변화 추이를 1초 미만의 지연 시간으로 조회하고 싶어한다 (InfluxDB).
- **STORY-02**: 개발자는 Kafka로 인입되는 스트림 데이터를 실시간으로 변환(JOIN/Windowing)하여 새로운 분석용 이벤트를 생성하고 싶어한다 (ksqlDB).
- **STORY-03**: 운영자는 수집된 마이크로서비스 로그에서 특정 키워드를 기반으로 초 단위의 고속 검색을 수행하고 싶어한다 (OpenSearch).
- **STORY-04**: 분석가는 수억 건의 레코드가 포함된 데이터웨어하우스에서 복잡한 SQL JOIN 쿼리를 실시간으로 수행하고 싶어한다 (StarRocks).

## Functional Requirements

- **REQ-PRD-FUN-01**: 시계열 데이터(TSDB)를 위한 전용 쓰기 및 조회 인터페이스 제공.
- **REQ-PRD-FUN-02**: SQL 문법을 이용한 실시간 스트림 처리 엔진(Stream Processing) 구축.
- **REQ-PRD-FUN-03**: 전문 검색(Full-text Search) 및 로그 수집 파이프라인 연동.
- **REQ-PRD-FUN-04**: 대규모 읽기 최적화 및 조인 성능을 보장하는 분석용 데이터웨어하우스 구축.

## Success Criteria

- **REQ-PRD-MET-01**: InfluxDB 조회 쿼리 P95 응답 속도 200ms 미만 유지.
- **REQ-PRD-MET-02**: OpenSearch 로그 인덱싱 지연 시간 5초 이내 보장.
- **REQ-PRD-MET-03**: StarRocks 대규모 조인 쿼리(1억 건 이상) 수행 시간 3초 이내 달성.

## Scope and Non-goals

- **In Scope**: InfluxDB, ksqlDB, OpenSearch, StarRocks의 요구사항 및 인터페이스 정의.
- **Out of Scope**: 개별 데이터 시각화 도구(Grafana)의 세부 대시보드 설계.
- **Non-goals**: 실시간 트랜잭션 수반 SQL 데이터 처리 (-> core PostgreSQL 담당).

## Risks, Dependencies, and Assumptions

- **Dependency**: 모든 분석 엔진은 `infra_net` 및 `${DEFAULT_DATA_DIR}` 환경에 의존함.
- **Risk**: 대규모 데이터 유입 시 분석 노드(Storage/Compute)의 리소스 부족 위험.
- **Assumption**: 원본 데이터는 핵심 데이터 티어 혹은 메시징 티어를 통해 안정적으로 공급됨.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: 분석용 스키마 조회, 로그 패턴 분석, SQL 쿼리 최적화 제안.
- **Disallowed Actions**: 원본 데이터 삭제, 운영 중인 분석 클러스터의 설정 무단 변경.

## Related Documents

- **ARD**: [0012-data-analytics-architecture.md](../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../04.specs/04-data-analytics/spec.md)
- **Guide**: [README.md](../07.guides/04-data/analytics/README.md)
