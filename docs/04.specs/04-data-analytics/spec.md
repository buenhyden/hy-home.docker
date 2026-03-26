# Analytics Tier Technical Specification (Spec)

> This document defines the technical specification for the specialized analytics data engines within the `04-data/analytics` sub-tier.

---

# Analytics Tier Specification

## Overview (KR)

이 문서는 `04-data/analytics` 티어의 시계열(InfluxDB), 스트림 처리(ksqlDB), 로그 검색(OpenSearch), OLAP 분석(StarRocks) 엔진들의 기술 설계 및 인터페이스 계약을 정의한다. 본 명세는 PRD-2026-03-26-04-data-analytics의 요구사항을 기술적으로 구체화하며, 인프라 계층과의 연동 및 데이터 처리 규약을 설명한다.

## Strategic Boundaries & Non-goals

- **Owns**: 개별 분석 엔진의 설정 계약, 데이터 보존 정책(Retention), 엔진 간 데이터 흐름 설계.
- **Non-goals**: 개별 비즈니스 로직에 종속된 쿼리 상세 설계 (Application 계층 담당), BI 도구의 시각화 레이아웃.

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-26-04-data-analytics.md]`
- **ARD**: `[../../02.ard/0012-data-analytics-architecture.md]`
- **Related ADRs**: `[../../03.adr/0015-analytics-engine-selection.md]`

## Contracts

- **Infrastructure Contract**:
  - 모든 엔진은 `infra_net` 브리지 네트워크에 배치되어야 한다.
  - 영구 데이터는 `${DEFAULT_DATA_DIR}/analytics/{engine_name}` 경로에 마운트되어야 한다.
- **Data / Interface Contract**:
  - InfluxDB: Line Protocol을 통한 수집 및 Flux/InfluxQL 쿼리 인터페이스.
  - ksqlDB: Kafka Topic 기반의 SQL 스트림 처리 인터페이스.
  - OpenSearch: REST API (Port 9200) 및 Lucene 기반 검색 인터페이스.
  - StarRocks: MySQL Protocol 호환 인터페이스 (Port 9030).
- **Governance Contract**:
  - 데이터 보존 기간(Retention Policy)은 각 엔진별 정책 설정 파일에서 중앙 관리한다.

## Core Design

- **Component Boundary**:
  - InfluxDB: Metrics & Time-series data hub.
  - ksqlDB: Real-time stream processing & transformation.
  - OpenSearch: Logging & full-text search engine.
  - StarRocks: Unified OLAP engine for complex analytical queries.
- **Key Dependencies**:
  - `04-data/core` (PostgreSQL): 원본 스냅샷 데이터 소스.
  - `05-messaging/rabbitmq`, `Kafka`: 실시간 데이터 수집 채널.
- **Tech Stack**: Docker, InfluxDB 2.x, ksqlDB, OpenSearch 2.x, StarRocks.

## Data Modeling & Storage Strategy

- **Schema Strategy**:
  - InfluxDB: Tag 기반 인덱싱 및 필드 중심 저장.
  - OpenSearch: 도메인별 인덱스 패턴 (e.g., `logs-*-*`).
  - StarRocks: OLAP 최적화를 위한 Star Schema 또는 Flat Table 모델 권장.
- **Retention Plan**:
  - 시계열 및 로그 데이터는 30일(기본) 보존 후 자동 삭제 또는 Cold storage 이동.

## Verification

```bash
# InfluxDB Health Check
curl -f http://influxdb:8086/health

# OpenSearch Status
curl -f http://opensearch:9200/

# StarRocks Connection test (via MySQL client)
mysql -h starrocks -P 9030 -u root
```

## Success Criteria & Verification Plan

- **VAL-SPC-04-ANA-01**: 모든 분석 엔진이 `infra_net` 내에서 상호 통신 가능해야 함.
- **VAL-SPC-04-ANA-02**: 영구 볼륨 마운트 후 컨테이너 재시작 시 데이터 무결성이 유지되어야 함.

## Related Documents

- **Guide**: `[../../07.guides/04-data/analytics/README.md]`
- **Runbook**: `[../../09.runbooks/04-data/analytics/influxdb.md]`
