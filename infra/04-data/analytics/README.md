# Analytics Tier (04-Data: Analytics)

> Analytical and specialized data engines for time-series, log search, stream processing, and OLAP.

## Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진을 관리한다. 시계열 데이터(InfluxDB), 실시간 스트림 처리(ksqlDB), 로그 검색 및 분석(OpenSearch), 그리고 대규모 OLAP 웨어하우스(StarRocks)를 포함하는 분석 데이터 계층을 담당한다.

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
├── ksql/           # Streaming SQL engine for Kafka
├── opensearch/     # Log Search & Analytics Engine
├── warehouses/     # StarRocks (OLAP) Engine
└── README.md       # This file
```

## How to Work in This Area

1. 신규 분석 엔진 추가 시 반드시 **ADR-0015** 기술 선택 기록을 먼저 확인한다.
2. 각 엔진 구성 변경 시 `infra_net` 보안 규약을 준수한다.
3. 운영 절차 변경 시 관련 런북(`docs/09.runbooks/04-data/analytics/`)을 함께 갱신한다.
4. 모든 비밀번호 및 토큰은 Docker Secrets( `secrets/` )로 관리한다.

## Related References

- **System Guide**: [docs/07.guides/04-data/analytics/](../../docs/07.guides/04-data/analytics/README.md)
- **Operations**: [docs/08.operations/04-data/analytics/](../../docs/08.operations/04-data/analytics/README.md)
- **Runbooks**: [docs/09.runbooks/04-data/analytics/](../../docs/09.runbooks/04-data/analytics/README.md)

## AI Agent Guidance

1. 이 README와 하위 디렉터리의 `README.md`를 우선적으로 읽어 각 엔진의 책임을 파악한다.
2. 인프라 변경 시 `docker-compose.yml`의 볼륨 마운트와 네트워크 설정을 확인한다.
3. `secrets/` 하위의 민감한 데이터는 직접 수정하지 말고 사용자에게 확인을 요청한다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
