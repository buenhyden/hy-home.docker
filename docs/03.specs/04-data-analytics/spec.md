---
status: active
---
<!-- Target: docs/03.specs/04-data-analytics/spec.md -->

# Analytics Tier Technical Specification (Spec)

> This document defines the technical specification for the specialized analytics data engines within the `04-data/analytics` sub-tier.

---

## Overview (KR)

이 문서는 `04-data/analytics` 티어의 시계열(InfluxDB), 스트림 처리(ksqlDB), 로그 검색(OpenSearch), OLAP 분석(StarRocks) 엔진들의 기술 설계 및 인터페이스 계약을 정의한다. 본 명세는 PRD-2026-03-26-04-data-analytics의 요구사항을 기술적으로 구체화하며, 인프라 계층과의 연동 및 데이터 처리 규약을 설명한다. 현재 root `docker-compose.yml`에서 일부 analytics include는 주석 처리되어 있으므로, 이 명세는 보유 구현과 optional integration boundary를 설명한다.

## Strategic Boundaries & Non-goals

- **Owns**: 개별 분석 엔진의 설정 계약, 데이터 보존 정책(Retention), 엔진 간 데이터 흐름 설계.
- **Non-goals**: 개별 비즈니스 로직에 종속된 쿼리 상세 설계 (Application 계층 담당), BI 도구의 시각화 레이아웃.

## Related Inputs

- **PRD**: [../../01.requirements/2026-03-26-04-data-analytics.md](../../01.requirements/2026-03-26-04-data-analytics.md)
- **ARD**: [../../02.architecture/requirements/0012-data-analytics-architecture.md](../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **Related ADRs**: [../../02.architecture/decisions/0015-analytics-engine-selection.md](../../02.architecture/decisions/0015-analytics-engine-selection.md)

## Contracts

- **Infrastructure Contract**:
  - Analytics compose files are present under `infra/04-data/analytics/`, while root compose includes for InfluxDB, ksqlDB, and OpenSearch are currently optional/commented.
  - StarRocks warehouses compose is standalone and not included by the root compose.
  - 모든 엔진은 `infra_net` 브리지 네트워크에 배치되어야 한다.
  - 영구 데이터는 bind-backed named volume으로 마운트되며, current compose device paths are service-specific under `${DEFAULT_DATA_DIR}` rather than a shared `analytics/` prefix.
- **Data / Interface Contract**:
  - InfluxDB: primary InfluxDB 3.x HTTP/Line Protocol + SQL query interface; legacy InfluxDB 2.x compose preserves Flux compatibility.
  - ksqlDB: Kafka Topic 기반의 SQL 스트림 처리 인터페이스.
  - OpenSearch: REST API (Port 9200) 및 Lucene 기반 검색 인터페이스.
  - StarRocks: MySQL Protocol 호환 인터페이스 (Port 9030).
- **Governance Contract**:
  - 데이터 보존 기간과 cleanup 기준은 operations policy/runbook에서 관리한다.
  - Retention is compose-enforced only when the linked service config declares it; otherwise it is an operational control requiring runtime evidence.

## Core Design

- **Component Boundary**:
  - InfluxDB: Metrics & Time-series data hub.
  - ksqlDB: Real-time stream processing & transformation.
  - OpenSearch: Logging & full-text search engine.
  - StarRocks: Unified OLAP engine for complex analytical queries.
- **Key Dependencies**:
  - `04-data/operational` and `04-data/relational`: 원본 스냅샷/트랜잭션 데이터 소스.
  - `05-messaging/kafka`: ksqlDB upstream broker, Schema Registry, and Kafka Connect dependency.
- **Tech Stack**: Docker, InfluxDB 3.x Core primary with InfluxDB 2.x legacy compose, Confluent ksqlDB 8.x, OpenSearch 3.x, StarRocks 4.x.

## Data Modeling & Storage Strategy

- **Schema Strategy**:
  - InfluxDB: Tag 기반 인덱싱 및 필드 중심 저장.
  - OpenSearch: 도메인별 인덱스 패턴 (e.g., `logs-*-*`).
  - StarRocks: OLAP 최적화를 위한 Star Schema 또는 Flat Table 모델 권장.
- **Retention Plan**:
  - 시계열, 로그, stream state, and OLAP data retention targets must be recorded per service before production-like use.
  - Automatic deletion or cold-storage movement is not assumed unless the current service config declares it.

## Interfaces & Data Structures

### Analytics Engine Contract

| Engine | Interface | Primary Data Shape | Persistence Boundary |
| --- | --- | --- | --- |
| InfluxDB | HTTP / Line Protocol | time-series measurements, tags, fields | `influxdb-data`, `influxdb-plugins` |
| ksqlDB | Kafka topics + SQL streams | stream/table definitions | `ksqldb-data-volume`, Kafka state stores, topic retention |
| OpenSearch | HTTPS REST API | index documents and mappings | `opensearch-data`, `opensearch-dashboards-data` |
| StarRocks | MySQL-compatible protocol | OLAP tables and materialized views | `starrocks-fe-data`, `starrocks-be-data` |

## Verification

```bash
# InfluxDB 3.x primary health check
curl -i http://influxdb:8181/

# InfluxDB 2.x legacy compose health check, only when docker-compose.v2.yml is selected
curl -f http://influxdb:8086/health

# OpenSearch status requires HTTPS and the admin Docker Secret
read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
curl -fsSk -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" https://opensearch:9200/_cluster/health
unset OPENSEARCH_ADMIN_PASSWORD

# StarRocks Connection test (via MySQL client)
mysql -h starrocks-fe -P 9030 -u root -e "SHOW FRONTENDS;"
```

## Success Criteria & Verification Plan

- **VAL-SPC-04-ANA-01**: 모든 분석 엔진이 `infra_net` 내에서 상호 통신 가능해야 함.
- **VAL-SPC-04-ANA-02**: 영구 볼륨 마운트 후 컨테이너 재시작 시 데이터 무결성이 유지되어야 함.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-22-data-analytics-execution-traceability.md](../../04.execution/plans/2026-05-22-data-analytics-execution-traceability.md)
- **Tasks**: [../../04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md](../../04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md)
- **Guide**: [../../05.operations/guides/04-data/analytics/README.md](../../05.operations/guides/04-data/analytics/README.md)
- **Policy**: [../../05.operations/policies/04-data/analytics/README.md](../../05.operations/policies/04-data/analytics/README.md)
- **Runbook**: [../../05.operations/runbooks/04-data/analytics/influxdb.md](../../05.operations/runbooks/04-data/analytics/influxdb.md)
