---
title: "Analytics Tier (04-data/analytics) Product Requirements"
version: "1.1.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "requirements"
artifact_id: "REQ-0005"
parent_ids: []
created: "2026-03-26"
---
# Analytics Tier (04-data/analytics) Product Requirements

> This document defines the product requirements for the specialized analytics data engines within the `04-data/analytics` sub-tier.

## Problem and Goals

본 문서는 플랫폼의 분석 요구사항을 정의한다. 시계열과 로그 검색은 `04-data/analytics`의 전용 엔진(InfluxDB, OpenSearch)이, 스트림 처리와 SQL·OLAP 분석은 `04-data/lakehouse`의 엔진(Flink, Trino)이 Iceberg table 위에서 맡는다(ADR-0039).

### Problem Statement

현재 구현은 `infra/04-data/analytics` 아래에 InfluxDB, OpenSearch compose를, `infra/04-data/lakehouse` 아래에 Flink, Trino compose를 보유한다. 이 PRD는 해당 엔진들이 core transactional data와 분리된 optional tier로 유지되어야 하며, root compose가 파일을 무조건 include하더라도 `core` profile에는 속하지 않아 별도 profile 선택 없이는 기동되지 않는다는 요구사항을 정의한다. 스트림 처리와 OLAP을 맡던 ksqlDB와 StarRocks는 SPEC-0180 S19에서 Flink와 Trino live acceptance(2026-09-24) 이후 제거되었다.

## Stakeholders and User Needs

플랫폼에서 발생하는 모든 정형/비정형 데이터를 실시간으로 수집, 가공, 분석하여 사용자에게 즉각적이고 심층적인 시각화 및 인사이트를 제공하는 고성능 분석 허브를 구축한다.

### Personas

- **Data Scientist**: Iceberg table에 대한 SQL·OLAP 조회로 트렌드를 도출해야 함.
- **SRE/DevOps**: 실시간 로그 검색 및 시스템 메트릭 모니터링이 필요함.
- **Home Automation User**: 실시간 차트와 센서 데이터의 변화를 지연 없이 확인하고 싶어함.

### Key Use Cases

- **STORY-01**: 사용자는 대시보드를 통해 지난 1년간의 스마트 홈 센서 데이터 변화 추이를 1초 미만의 지연 시간으로 조회하고 싶어한다 (InfluxDB).
- **STORY-02**: 운영자는 수집된 마이크로서비스 로그에서 특정 키워드를 기반으로 초 단위의 고속 검색을 수행하고 싶어한다 (OpenSearch).
- **STORY-03**: 데이터 엔지니어는 Kafka 이벤트를 SQL로 가공해 table에 쌓고, 같은 table을 SQL로 조회하고 싶어한다 (Flink, Trino).

## Functional Requirements

- **REQ-0005-FR-0001**: 시계열 데이터(TSDB)를 위한 전용 쓰기 및 조회 인터페이스 제공.
- **REQ-0005-FR-0003**: 전문 검색(Full-text Search) 및 로그 수집 파이프라인 연동.
- **REQ-0005-FR-0005**: SQL 기반 스트림 처리로 이벤트를 Iceberg table에 기록하며, 장애 뒤 마지막 checkpoint부터 이어서 처리한다.
- **REQ-0005-FR-0006**: Iceberg table에 대한 대화형 SQL·OLAP 조회를 제공한다.

FR 번호 0002(ksqlDB 스트림 처리)와 0004(StarRocks OLAP)는 엔진 제거와 함께 retire되었고 재사용하지 않는다. 같은 필요는 0005와 0006이 엔진 중립적으로 다시 정의한다.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0005-FR-0001**: InfluxDB 3 Core 단일 compose, database 이름, port `8181`, `/api/v3/write_lp` endpoint/schema, current healthcheck가 문서와 정적 source에서 일치해야 한다. Token provisioning과 authenticated write acceptance는 별도 runtime 승인 전까지 검증된 것으로 간주하지 않는다.
- **REQ-0005-FR-0003**: OpenSearch 문서는 현재 compose가 증명하는 단일 primary stack, profile이 선택하는 cluster topology, secret/volume/healthcheck 경계를 과장 없이 설명해야 한다. live 성능 수치(P95, indexing latency)는 별도 runtime benchmark evidence가 있을 때만 success evidence로 기록한다.
- **REQ-0005-FR-0005**: Flink가 batch INSERT와 checkpoint를 거치는 streaming INSERT로 Iceberg table을 쓰고, checkpoint가 host directory에 기록되어야 한다. 2026-09-24 live acceptance에서 통과했다(SPEC-0180 Task 0008).
- **REQ-0005-FR-0006**: Trino가 Flink가 쓴 같은 table을 읽고, Great Expectations suite가 Trino를 통해 통과해야 한다. 2026-09-24 live acceptance에서 통과했다. 대화형 성능 수치는 별도 benchmark evidence가 있을 때만 기록한다.

## Constraints

- **In Scope**: InfluxDB, OpenSearch, Flink, Trino의 분석 요구사항, 인터페이스, optional compose 실행 경계 정의.
- **Owned elsewhere**: Iceberg catalog, table bucket과 SeaweedFS 저장소 운영은 SPEC-0180과 POL-0094가 소유한다.
- **Out of Scope**: 개별 데이터 시각화 도구(Grafana)의 세부 대시보드 설계.
- **Non-goals**: 실시간 트랜잭션 수반 SQL 데이터 처리 (-> core PostgreSQL 담당).

### AI Agent Requirements

- **Allowed Actions**: 분석용 스키마 조회, 로그 패턴 분석, SQL 쿼리 최적화 제안.
- **Disallowed Actions**: 원본 데이터 삭제, 운영 중인 분석 클러스터의 설정 무단 변경.

## Risks

- **Dependency**: 모든 분석 엔진은 선언된 network, compose profile, bind-backed named volume, Docker Secrets에 의존하며, lakehouse 엔진은 SeaweedFS의 Iceberg catalog와 Kafka(스트림 입력)에도 의존함.
- **Risk**: 대규모 데이터 유입 시 분석 노드(Storage/Compute)의 리소스 부족 위험.
- **Assumption**: 원본 데이터는 핵심 데이터 티어 혹은 메시징 티어를 통해 안정적으로 공급됨.

## Traceability

- **Architecture Description**: [0012-data-analytics-architecture.md](../02.architecture/descriptions/0012-data-analytics-architecture.md)
- **ADR**: [0039-analytics-engines-after-lakehouse-convergence.md](../02.architecture/decisions/0039-analytics-engines-after-lakehouse-convergence.md) (supersedes ADR-0015)
- **Spec**: [SPEC-0180](../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md) (lakehouse 도입과 ksqlDB·StarRocks 제거)
- **Guide**: [README.md](../05.operations/catalog/04-data/README.md)
