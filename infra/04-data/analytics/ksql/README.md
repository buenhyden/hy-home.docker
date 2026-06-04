# ksqlDB

> Streaming SQL engine for Apache Kafka.

## Overview (KR)

ksqlDB는 익숙한 SQL 구문을 사용하여 실시간 스트림 처리 애플리케이션을 구축할 수 있게 한다. Kafka 클러스터 및 Schema Registry와 직접 통합되어 실시간 분석 및 데이터 변환을 수행한다.

## Audience

이 README의 주요 독자:

- **Developers**: 스트림 처리 애플리케이션 개발
- **Operators**: 자원 관리 및 성능 모니터링
- **Architects**: 시스템 설계 및 통합 전략 수립
- **AI Agents**: 인프라 탐색 및 스트림 로직 분석

## Scope

### In Scope

- SQL을 이용한 실시간 스트림 처리
- Kafka 브로커 및 Schema Registry와의 통합
- 테스트 및 예제를 위한 데이터 생성 도구
- ksqlDB 서버 및 CLI 관리

### Out of Scope

- 핵심 Kafka 클러스터 관리 (-> `infra/05-messaging/kafka` 담당)
- Schema Registry 내부 관리 규약
- 장기 데이터 영속성 (-> InfluxDB 또는 PostgreSQL 담당)

## Structure

```text
ksql/
├── docker-compose.yml       # Primary Deployment (ksqlDB Server & CLI)
└── README.md                # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | ksqlDB service leaf in `04-data`; services: `ksqldb-server`, `ksqldb-cli`, `ksql-datagen`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/ksql/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `KSQL_CONFIG_DIR`, `KSQL_BOOTSTRAP_SERVERS`, `KSQL_HOST_NAME`, `KSQL_LISTENERS`, `KSQL_CACHE_MAX_BYTES_BUFFERING`, `KSQL_KSQL_SCHEMA_REGISTRY_URL`, `KSQL_PRODUCER_INTERCEPTOR_CLASSES`, `KSQL_CONSUMER_INTERCEPTOR_CLASSES`, plus 8 more; profiles: `data`, `ksql` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/ksql/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `ksqldb-data-volume:/var/lib/ksql:rw`, `ksqldb-data-volume` |
| Ports | `${KSQLDB_HOST_PORT:-8088}:${KSQLDB_PORT:-8088}` |
| Labels | `hy-home.tier` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `ksqldb-server`; not declared for `ksqldb-cli`, `ksql-datagen` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/analytics/ksqldb.md), [Policy](../../../../docs/05.operations/policies/04-data/analytics/ksqldb.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/analytics/ksqldb.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with linked repository validators and service logs; service-local compose parsing requires root network context or a local validation overlay. |

## How to Work in This Area

1. 아키텍처 및 사용법은 [ksqlDB 시스템 가이드](../../../../docs/05.operations/guides/04-data/analytics/ksqldb.md)를 참조한다.
2. 처리 규약 및 자원 할당은 [운영 정책](../../../../docs/05.operations/policies/04-data/analytics/ksqldb.md)을 따른다.
3. 스트림 지연이나 연결 이슈 발생 시 [복구 런북](../../../../docs/05.operations/runbooks/04-data/analytics/ksqldb.md)을 참조한다.
4. ksqlDB를 시작하기 전에 Kafka 브로커와 Schema Registry의 상태를 확인한다.

## Validation

- Run `bash scripts/validation/check-doc-implementation-alignment.sh` after README or Compose reference changes that affect ksqlDB.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with repository validators and `docker logs ksqldb-server` for runtime evidence. Service-local compose config requires root network context or a local validation overlay.
- Check ksqlDB logs for broker connectivity or stream startup errors before changing Compose settings.

## Related Documents

- **System Guide**: [docs/05.operations/04-data/analytics/ksqldb.md](../../../../docs/05.operations/guides/04-data/analytics/ksqldb.md)
- **Policy**: [docs/05.operations/policies/04-data/analytics/ksqldb.md](../../../../docs/05.operations/policies/04-data/analytics/ksqldb.md)
- **Runbook**: [docs/05.operations/runbooks/04-data/analytics/ksqldb.md](../../../../docs/05.operations/runbooks/04-data/analytics/ksqldb.md)
- **Kafka Status**: `infra/05-messaging/kafka/README.md`

## AI Agent Guidance

1. ksqlDB 쿼리를 작성하거나 수정하기 전에 Kafka 토픽 구조를 먼저 파악한다.
2. 서비스 재시작 시 스트림 처리 오프셋(Offset) 영향을 고려한다.
3. 구성 변경 시 Kafka 브로커와의 네트워크 가시성을 확인한다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
