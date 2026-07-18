# InfluxDB (TSDB)

> High-performance time series database for metrics and analytics.

## Overview (KR)

`influxdb` 서비스는 `hy-home.docker`의 시계열 데이터 영속성 계층을 제공한다. 현재 구현은 InfluxDB 3 Core 단일 compose이며 SQL 조회와 HTTP line-protocol 쓰기의 source interface를 정의한다.

## Audience

이 README의 주요 독자:

- **Developers**: 지표 통합 및 데이터 연동
- **Operators**: 자원 관리 및 성능 튜닝
- **AI Agents**: 인프라 탐색 및 메트릭 분석

## Scope

### In Scope

- 관측성을 위한 시계열 데이터 영속성
- InfluxDB 3 Core database와 line-protocol write endpoint source 계약 확인
- 별도 runtime 승인이 필요한 token provisioning 경계 확인
- bind-backed named volume 기반 data/plugin persistence 확인

### Out of Scope

- 장기 로그 저장 (-> Loki 담당)
- 객체 저장 (-> MinIO 담당)
- 실시간 스트림 처리 (-> ksqlDB 담당)

## Structure

```text
influxdb/
├── docker-compose.yml       # InfluxDB 3 Core deployment
└── README.md                # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | InfluxDB (TSDB) service leaf in `04-data`; primary service: `influxdb`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/influxdb/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | profile: `data`; database key: `INFLUXDB_DB_NAME` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) |
| Networks | `infra_net` |
| Volumes | `influxdb-data:/var/lib/influxdb3/data:rw`, `influxdb-plugins:/var/lib/influxdb3/plugins:rw` |
| Ports | No host port declared; Traefik service port `${INFLUXDB_PORT:-8181}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.influxdb.rule`, `traefik.http.routers.influxdb.entrypoints`, `traefik.http.routers.influxdb.tls`, `traefik.http.routers.influxdb.middlewares`, `traefik.http.services.influxdb.loadbalancer.server.port` |
| Secret refs | Root Compose declares `influxdb_api_token` and `influxdb_password` as repository metadata, but root declarations and metadata are not leaf server wiring; this leaf mounts neither secret and does not provision a server token |
| Write API | `POST http://influxdb:8181/api/v3/write_lp?db=${INFLUXDB_DB_NAME}` requires an authorized operator/named token; token creation/provisioning and authenticated write acceptance require separate runtime approval and remain unverified |
| Healthcheck | Probes `http://127.0.0.1:8181/` and accepts `200`, `204`, or `401` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/analytics/influxdb.md), [Policy](../../../../docs/05.operations/policies/04-data/analytics/influxdb.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/analytics/influxdb.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with linked repository validators and service logs; service-local compose parsing requires root network/secret context or a local validation overlay. |

## How to Work in This Area

1. 아키텍처 세부 사항은 [InfluxDB 시스템 가이드](../../../../docs/05.operations/guides/04-data/analytics/influxdb.md)를 참조한다.
2. 데이터 보존 및 보안 규약은 [운영 정책](../../../../docs/05.operations/policies/04-data/analytics/influxdb.md)을 따른다.
3. 수집 장애 발생 시 [복구 런북](../../../../docs/05.operations/runbooks/04-data/analytics/influxdb.md)을 참조한다.
4. Root secret declarations are metadata only. Source-only validation cannot prove authorization; token creation/provisioning and authenticated write acceptance require separate runtime approval.

## Validation

- Run `bash scripts/validation/check-doc-implementation-alignment.sh` after README or Compose reference changes that affect InfluxDB.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with repository validators and `docker logs influxdb` for runtime evidence. Service-local compose config requires root network/secret context or a local validation overlay.
- Do not diagnose writes from a presumed secret path. Escalate for approved token provisioning and authenticated write acceptance before changing retention, database, or version settings.

## Related Documents

- **System Guide**: [docs/05.operations/04-data/analytics/influxdb.md](../../../../docs/05.operations/guides/04-data/analytics/influxdb.md)
- **Policy**: [docs/05.operations/policies/04-data/analytics/influxdb.md](../../../../docs/05.operations/policies/04-data/analytics/influxdb.md)
- **Runbook**: [docs/05.operations/runbooks/04-data/analytics/influxdb.md](../../../../docs/05.operations/runbooks/04-data/analytics/influxdb.md)
- **Official token administration**: [InfluxDB 3 Core token management](https://docs.influxdata.com/influxdb3/core/admin/tokens/)
- **Monitoring**: `https://grafana.${DEFAULT_URL}`

## AI Agent Guidance

1. 이 README를 읽고 InfluxDB 3 Core의 database/endpoint source contract와 token-provisioning 승인 경계를 파악한다.
2. Token provisioning은 별도 runtime 승인과 인증 쓰기 acceptance evidence 없이는 완료로 간주하지 않는다.
3. 데이터 보존 정책을 수정하기 전에 반드시 운영 정책 문서를 대조한다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
