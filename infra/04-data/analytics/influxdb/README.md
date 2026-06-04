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
- InfluxDB 3.x Core primary compose와 InfluxDB 2.x legacy compose 구분
- Docker Secret 기반 API token/password mount 확인
- bind-backed named volume 기반 data/plugin persistence 확인

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

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | InfluxDB (TSDB) service leaf in `04-data`; primary service: `influxdb`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/influxdb/docker-compose.yml` |
| Config files | `docker-compose.v2.yml`, `docker-compose.yml` |
| Config values | primary profile: `data`; legacy v2 init env keys are only in `docker-compose.v2.yml` |
| Compose linkage | primary compose root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml); `docker-compose.v2.yml` is a local legacy variant |
| Networks | `infra_net` |
| Volumes | `influxdb-data:/var/lib/influxdb2:rw`, `influxdb-data`, `influxdb-data:/var/lib/influxdb3/data:rw`, `influxdb-plugins:/var/lib/influxdb3/plugins:rw`, `influxdb-plugins` |
| Ports | No host port declared; Traefik service port `${INFLUXDB_PORT:-8181}` for primary v3 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.influxdb.rule`, `traefik.http.routers.influxdb.entrypoints`, `traefik.http.routers.influxdb.tls`, `traefik.http.routers.influxdb.middlewares`, `traefik.http.services.influxdb.loadbalancer.server.port` |
| Secret refs | names: `influxdb_password`, `influxdb_api_token`; mounts: `/run/secrets/influxdb_password`, `/run/secrets/influxdb_api_token` |
| Healthcheck | Primary v3 healthcheck probes `http://127.0.0.1:8181/` and accepts `200`, `204`, or `401`; legacy v2 healthcheck probes `/health` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/analytics/influxdb.md), [Policy](../../../../docs/05.operations/policies/04-data/analytics/influxdb.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/analytics/influxdb.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with linked repository validators and service logs; service-local compose parsing requires root network/secret context or a local validation overlay. |

## How to Work in This Area

1. 아키텍처 세부 사항은 [InfluxDB 시스템 가이드](../../../../docs/05.operations/guides/04-data/analytics/influxdb.md)를 참조한다.
2. 데이터 보존 및 보안 규약은 [운영 정책](../../../../docs/05.operations/policies/04-data/analytics/influxdb.md)을 따른다.
3. 수집 장애 발생 시 [복구 런북](../../../../docs/05.operations/runbooks/04-data/analytics/influxdb.md)을 참조한다.
4. API token evidence는 Docker Secret `influxdb_api_token`과 mount path `/run/secrets/influxdb_api_token` 기준으로 확인한다. Secret value는 출력하지 않는다.

## Validation

- Run `bash scripts/validation/check-doc-implementation-alignment.sh` after README or Compose reference changes that affect InfluxDB.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with repository validators and `docker logs influxdb` for runtime evidence. Service-local compose config requires root network/secret context or a local validation overlay.
- If writes fail, inspect `docker compose logs influxdb` and confirm the expected API token secret path exists before changing retention, database, or version settings.

## Related Documents

- **System Guide**: [docs/05.operations/04-data/analytics/influxdb.md](../../../../docs/05.operations/guides/04-data/analytics/influxdb.md)
- **Policy**: [docs/05.operations/policies/04-data/analytics/influxdb.md](../../../../docs/05.operations/policies/04-data/analytics/influxdb.md)
- **Runbook**: [docs/05.operations/runbooks/04-data/analytics/influxdb.md](../../../../docs/05.operations/runbooks/04-data/analytics/influxdb.md)
- **Monitoring**: `https://grafana.${DEFAULT_URL}`

## AI Agent Guidance

1. 이 README를 읽고 InfluxDB의 책임 범위와 버전 차이를 파악한다.
2. 토큰 및 비밀번호 변경 시 Docker Secrets 설정을 우선적으로 확인한다.
3. 데이터 보존 정책을 수정하기 전에 반드시 운영 정책 문서를 대조한다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
