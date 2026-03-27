# InfluxDB (TSDB)

> High-performance time series database for metrics and analytics.

## Overview (KR)

`influxdb` 서비스는 `hy-home.docker`의 시계열 데이터 영속성 계층을 제공한다. 높은 수집률과 Flux/SQL을 통한 분석 쿼리를 지원하며, 성능 지표 및 관측성 데이터를 저장하는 데 사용된다. 본 구현체는 조건부 설정을 통해 InfluxDB 3.x(Core)와 2.x(Legacy)를 모두 지원한다.

## Audience

이 README의 주요 독자:

- **Developers**: 지표 통합 및 데이터 연동
- **Operators**: 자원 관리 및 성능 튜닝
- **AI Agents**: 인프라 탐색 및 메트릭 분석

## Scope

### In Scope

- 관측성을 위한 시계열 데이터 영속성
- Telegraf, k6, Locust 등을 통한 메트릭 수집
- Grafana를 위한 데이터 소스 제공
- InfluxDB 버킷 및 보존 정책(Retention Policy) 관리

### Out of Scope

- 장기 로그 저장 (-> Loki 담당)
- 객체 저장 (-> MinIO 담당)
- 실시간 스트림 처리 (-> ksqlDB 담당)

## Structure

```text
influxdb/
├── docker-compose.yml       # Primary Deployment (InfluxDB 3.x)
├── docker-compose.v2.yml    # Legacy Deployment (InfluxDB 2.x)
└── README.md                # This file
```

## How to Work in This Area

1. 아키텍처 세부 사항은 [InfluxDB 시스템 가이드](../../../docs/07.guides/04-data/analytics/influxdb.md)를 참조한다.
2. 데이터 보존 및 보안 규약은 [운영 정책](../../../docs/08.operations/04-data/analytics/influxdb.md)을 따른다.
3. 수집 장애 발생 시 [복구 런북](../../../docs/09.runbooks/04-data/analytics/influxdb.md)을 참조한다.
4. 모든 API 토큰은 `secrets/influxdb_api_token`에 정의되어야 한다.

## Related References

- **System Guide**: [docs/07.guides/04-data/analytics/influxdb.md](../../../docs/07.guides/04-data/analytics/influxdb.md)
- **Operations**: [docs/08.operations/04-data/analytics/influxdb.md](../../../docs/08.operations/04-data/analytics/influxdb.md)
- **Runbook**: [docs/09.runbooks/04-data/analytics/influxdb.md](../../../docs/09.runbooks/04-data/analytics/influxdb.md)
- **Monitoring**: `https://grafana.${DEFAULT_URL}`

## AI Agent Guidance

1. 이 README를 읽고 InfluxDB의 책임 범위와 버전 차이를 파악한다.
2. 토큰 및 비밀번호 변경 시 Docker Secrets 설정을 우선적으로 확인한다.
3. 데이터 보존 정책을 수정하기 전에 반드시 운영 정책 문서를 대조한다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
