---
status: active
---

<!-- Target: docs/05.operations/guides/env-key-comparison.md -->

# `.env.example` vs `.env` Key Comparison

> **중요**: 이 문서는 키 이름과 구조만 기록한다. 실제 값은 포함하지 않는다.

## Overview (KR)

이 문서는 `.env.example`과 `.env`의 환경변수 키 일관성을 확인하는 운영 참조 문서다. 키셋 동기화 여부, 순서 차이, 누락·추가·deprecated 키를 기록한다.

## Usage

이 문서는 `.env.example`과 `.env`의 키 동기화 상태를 확인할 때 참조한다. 값은 포함하지 않으므로 공개 저장소에서 안전하게 열람 가능하다. 신규 서비스 추가 시 `.env.example`에 먼저 키를 추가하고, `.env`에도 동기화한다. 주기 점검은 `## 점검 주기` 섹션을 따른다.

## Common Checks

- `.env.example`과 `.env`의 라인 수가 동일한지 확인한다.
- 아래 요약 표에서 "한쪽에만 존재" 항목이 없는지 확인한다.
- 새 서비스 추가 후 `grep -c '=' .env.example` 결과를 이전 값과 비교한다.

## 감사 기준일

2026-05-26

## 요약

| 항목                    | 결과                                          |
| ----------------------- | --------------------------------------------- |
| `.env.example` 키 수    | 281                                           |
| `.env` 키 수            | 281                                           |
| 키셋 동일 여부          | ✓ 동일 (순서 차이만 있음)                     |
| `.env.example`에만 존재 | 없음                                          |
| `.env`에만 존재         | 없음                                          |
| 순서 차이               | `KAFKA_EXTERNAL_HOSTNAME`, `QDRANT_GRPC_PORT` |

## 상세 분석

### 순서 차이 (실질적 영향 없음)

두 파일의 키셋은 동일하지만 다음 두 키의 위치가 다르다.

| 키                        | `.env.example` 위치         | `.env` 위치          | 영향 |
| ------------------------- | --------------------------- | -------------------- | ---- |
| `KAFKA_EXTERNAL_HOSTNAME` | 143번째 키 (Kafka 섹션 내)  | 281번째 키 (파일 끝) | 없음 |
| `QDRANT_GRPC_PORT`        | 234번째 키 (Qdrant 섹션 내) | 280번째 키 (파일 끝) | 없음 |

순서 차이는 Docker Compose 동작에 영향을 미치지 않는다. `.env`를 `.env.example` 순서와 동기화하려면 해당 키를 올바른 섹션으로 이동하면 된다.

### 누락 키

없음.

### 추가 키 (`.env`에만 존재)

없음.

### Deprecated / 불명확 키

| 키                        | 상태        | 비고                     |
| ------------------------- | ----------- | ------------------------ |
| `KAFKA_EXTERNAL_HOSTNAME` | 순서 불일치 | Kafka 섹션 내 위치 권장  |
| `QDRANT_GRPC_PORT`        | 순서 불일치 | Qdrant 섹션 내 위치 권장 |

## 키 카테고리 현황

| 카테고리               | `.env.example` 그룹                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| Global & Project       | `DEFAULT_URL`, `DEFAULT_TIMEZONE`                                                                 |
| Infrastructure Network | `INFRA_SUBNET`, `INFRA_GATEWAY`, `KEYCLOAK_IP`, `PROJECT_NET_NAME`, `HYHOME_EXTERNAL_NET_NAME`    |
| Volume & Project Paths | `DEFAULT_DOCKER_PROJECT_PATH` 외 10개 마운트 경로                                                 |
| Gateway (Traefik)      | `HTTP_PORT`, `HTTPS_PORT`, `TRAEFIK_*` (8개)                                                      |
| Identity & Access      | `KEYCLOAK_*`, `OAUTH2_*`, `GRAFANA_PROXY_CLIENT_ID`, `KAFBAT_OAUTH_CLIENT_ID`                     |
| PostgreSQL / Patroni   | `POSTGRES_*`, `HAPROXY_*`, `PATRONI_*`, `SUPABASE_*` (32개)                                       |
| NoSQL & Cache          | `VALKEY_*`, `REDIS_*`, `MONGODB_*`, `COUCHDB_*`, `CASSANDRA_*`, `INFLUXDB_*`, `NEO4J_*`, `ETCD_*` |
| Message Brokers        | `KAFKA_*`, `RABBITMQ_*`                                                                           |
| Object Storage         | `MINIO_*`, `SEAWEEDFS_*`                                                                          |
| Observability          | `PROMETHEUS_*`, `GRAFANA_*`, `LOKI_*`, `TEMPO_*`, `ALLOY_*`, `PYROSCOPE_*`                        |
| Search & Analytics     | `ES_*`, `OPENSEARCH_*`                                                                            |
| Automation & AI        | `AIRFLOW_*`, `N8N_*`, `TERRAKUBE_*`, `LOCUST_*`, `OLLAMA_*`, `QDRANT_*`                           |
| Security & Tooling     | `VAULT_*`, `SONARQUBE_*`, `STALWART_*`, `SYNCTHING_*`, `REGISTRY_*`                               |
| Management             | `REDIS_INSIGHT_*`, `PORTAINER_*`, `HOMER_*`, `DOZZLE_*`, `OPEN_NOTEBOOK_*`, `SURREALDB_*`         |
| Lab                    | `LAB_ALLOWED_CIDRS`                                                                               |

## 점검 주기

분기 1회 또는 서비스 추가/제거 시. 점검 후 이 문서의 "감사 기준일"과 요약 표를 업데이트한다.

## Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없습니다.

## Related Documents

- [Secrets Key Comparison](./sensitive-env-vars-comparison.md)
- [Spec](../../03.specs/workspace-audit-2026-05/spec.md)
- [secrets/README.md](../../../secrets/README.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
