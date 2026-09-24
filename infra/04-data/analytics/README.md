---
title: "Analytics Tier (04-Data: Analytics)"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-24"
created: "2026-03-27"
---

# Analytics Tier (04-Data: Analytics)

> Analytical and specialized data engines for time-series, log search, stream processing, and OLAP.

## Overview

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진을 관리한다. 시계열 데이터(InfluxDB)와 로그 검색 및 분석(OpenSearch)을 포함하는 분석 데이터 계층을 담당한다. 실시간 스트림 처리와 대규모 OLAP 웨어하우스는 `lakehouse` (Flink, Trino)가 담당한다.

## Audience

이 README의 주요 독자:

- **Architects**: 데이터 분석 파이프라인 설계 및 엔진 선택
- **Operators**: 분석 노드 상태 점검 및 자원 관리
- **Data Engineers**: 분석 스키마 및 쿼리 인터페이스 활용
- **AI Agents**: 분석 데이터 추출 및 시스템 구성 탐색

## Scope

### In Scope

- 분석 엔진 인프라 구성 (Docker Compose)
- 영구 데이터 관리 및 볼륨 영속성
- 데이터 보존 정책 및 분석을 위한 네트워크 설정
- 엔진별 기본 설정 및 운영 도구

### Out of Scope

- 핵심 트랜잭션 관계형 DB (-> `04-data/relational` 담당)
- 시각화 대시보드 UI 설계 (-> Grafana 담당)
- 외부 데이터 소스와의 ETL 로직 개발

## Structure

```text
analytics/
├── influxdb/       # Time Series Database (TSDB)
├── opensearch/     # Log Search & Analytics Engine
└── README.md       # This file
```

## How to Work in This Area

| Package | Classification | Exact profile | Stage 05 subject |
| --- | --- | --- | --- |
| [InfluxDB](influxdb/README.md) | `OPTIONAL` | `influxdb` | `0017-influxdb` |
| [OpenSearch](opensearch/README.md) | `OPTIONAL` primary / `LAB` cluster | `opensearch` / `opensearch-cluster` | `0019-opensearch` |

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. 신규 분석 엔진 추가 시 반드시 **ADR-0015** 기술 선택 기록을 먼저 확인한다.
2. 각 엔진 구성 변경 시 network 소속 규약(GDE-0077)을 준수한다.
3. 운영 절차 변경 시 관련 guide/policy/runbook(`docs/05.operations/catalog/04-data/`)을 함께 갱신한다.
4. Docker Secrets는 compose에 선언된 서비스에서만 current implementation evidence로 취급한다. InfluxDB and OpenSearch declare secrets.

5. 이 README와 하위 디렉터리의 `README.md`를 우선적으로 읽어 각 엔진의 책임을 파악한다.
6. 인프라 변경 시 `docker-compose.yml`의 볼륨 마운트와 네트워크 설정을 확인한다.
7. `secrets/` 하위의 민감한 데이터는 직접 수정하지 말고 사용자에게 확인을 요청한다.

## Related Documents

- Stage 05 subjects: `docs/05.operations/catalog/04-data/<subject>/`
- [Documentation index](../../../docs/README.md)

---
Copyright (c) 2026. Analytics Tier Infrastructure.

Runtime pins are owned by the Compose/Dockerfile declarations; the [derived Compose image projection](../../tech-stack.versions.json) provides drift verification.
