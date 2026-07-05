# Kafka Event Streaming (05-messaging)

> Kafka KRaft event streaming for hy-home.docker.

## Overview

The platform's primary event streaming backbone. Root `docker-compose.yml` includes `docker-compose.dev.yml`, which renders a single broker development stack. `docker-compose.yml` in this directory is the full 3 broker Kafka compose and requires root network/secret context when validated service-locally.

## Audience

이 README의 주요 독자:

- **Data Engineers**: 데이터 파이프라인 및 커넥터 구성.
- **Backend Developers**: 이벤트 기반 아키텍처 및 메시지 생산/소비.
- **Operators**: 클러스터 상태 모니터링 및 브로커 관리.
- **AI Agents**: 실시간 이벤트 분석 및 자동화된 토픽 관리.

## Scope

### In Scope

- **Root dev Kafka Broker**: KRaft 기반 단일 broker 개발 구성(`docker-compose.dev.yml`).
- **Full Kafka Broker Cluster**: KRaft 기반 3 broker compose(`docker-compose.yml`).
- **Confluent Schema Registry**: Avro/JSON 스키마 버전 관리.
- **Kafka Connect**: 외부 시스템 연동용 커넥터 실행 엔진.
- **Kafbat UI**: 웹 기반 관리 대시보드.
- **Observability**: JMX 및 Prometheus Exporter를 통한 지표 수집.

### Out of Scope

- 개별 마이크로서비스의 Consumer/Producer 로직.
- 커스텀 Kafka Connector 개발 (Java SDK 영역).
- 외부 클라우드 관리형 Kafka (MSK/Confluent Cloud) 연동.

## Structure

```text
kafka/
├── jmx-exporter/       # JMX to Prometheus metrics config
├── kafbat-ui/          # UI configuration
├── docker-compose.yml  # Kafka ecosystem orchestration
└── README.md          # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Kafka Event Streaming service leaf in `05-messaging`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/05-messaging/kafka/docker-compose.dev.yml`; local full compose: `docker-compose.yml` |
| Config files | `docker-compose.dev.yml`, `docker-compose.yml` |
| Config values | root dev env keys include `CLUSTER_ID`, `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1`, `KAFKA_PROCESS_ROLES`, `KAFKA_CONTROLLER_QUORUM_VOTERS`; full compose uses broker IDs 1-3 and replication factor 3 for internal topics; profiles: `messaging`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/05-messaging/kafka/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `kafka-1-data:/var/lib/kafka/data:rw`, `./jmx-exporter:/usr/share/jmx_exporter:ro`, `kafka-connect-data:/var/lib/kafka-connect:rw`, `./kafbat-ui/dynamic_config.template.yaml:/tmp/dynamic_config.template.yaml:ro`, `kafka-1-data`, `kafka-connect-data`, `kafka-2-data:/var/lib/kafka/data:rw`, `kafka-3-data:/var/lib/kafka/data:rw`, plus 2 more |
| Ports | `${KAFKA_EXTERNAL_1_HOST_PORT:-9092}:${KAFKA_EXTERNAL_PORT:-9092}`, `${KAFKA_JMX_1_HOST_PORT:-19101}:${KAFKA_JMX_PORT:-9101}`, `${KAFKA_JMX_EXPORTER_1_HOST_PORT:-19404}:${KAFKA_JMX_EXPORTER_PORT:-9404}`, `${SCHEMA_REGISTRY_PORT:-8081}`, `${KAFKA_EXTERNAL_2_HOST_PORT:-9094}:${KAFKA_EXTERNAL_PORT:-9092}`, `${KAFKA_JMX_2_HOST_PORT:-29101}:${KAFKA_JMX_PORT:-9101}`, `${KAFKA_JMX_EXPORTER_2_HOST_PORT:-29404}:${KAFKA_JMX_EXPORTER_PORT:-9404}`, `${KAFKA_EXTERNAL_3_HOST_PORT:-9096}:${KAFKA_EXTERNAL_PORT:-9092}`, plus 2 more |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.schema-registry.rule`, `traefik.http.routers.schema-registry.entrypoints`, `traefik.http.routers.schema-registry.tls`, `traefik.http.routers.schema-registry.middlewares`, `traefik.http.services.schema-registry.loadbalancer.server.port`, `traefik.http.routers.kafka-connect.rule`, plus 14 more |
| Secret refs | names: `kafbat_client_secret`; mounts: `/run/secrets/kafbat_client_secret` |
| Healthcheck | Compose healthcheck declared for Kafka broker(s), `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, and `kafka-exporter`; `kafka-init` is a job and has no healthcheck |
| Operations | [Guide](../../../docs/05.operations/guides/05-messaging/kafka.md), [Policy](../../../docs/05.operations/policies/05-messaging/kafka.md), [Runbook](../../../docs/05.operations/runbooks/05-messaging/kafka.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **Bootstrap**: [Kafka KRaft Guide](../../../docs/05.operations/guides/05-messaging/kafka.md)를 읽고 클러스터 초기 구성 방식을 파악한다.
2. **Configuration**: root dev는 `docker-compose.dev.yml`, full cluster는 `docker-compose.yml`의 Broker ID 및 포트 매핑 설정을 확인한다.
3. **Execution**: 변경 사항 적용 후 repository root에서 root profile 검증을 먼저 수행한다.
4. **Validation**: [Messaging Runbook](../../../docs/05.operations/runbooks/05-messaging/kafka.md)의 점검 절차를 수행한다.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Engine     | Confluent CP-Kafka             | 8.3.0                     |
| Mode       | KRaft                          | Integrated Metadata log   |
| Registry   | CP-Schema-Registry             | 8.3.0                     |
| UI         | Kafbat (Kafka UI)              | Web-based management      |
| Exporter   | Kafka Exporter                 | `danielqsj/kafka-exporter:v1.9.0` |

## Configuration

### Environment Variables

| Variable | Node 1 | Node 2 | Node 3 | Description |
| :--- | :--- | :--- | :--- | :--- |
| `KAFKA_EXTERNAL_PORT` | 9092 | 9094 | 9096 | 외부 클라이언트 접속 포트 |
| `KAFKA_NODE_ID` | 1 | 2 | 3 | 클러스터 내 고유 노드 ID |
| `CLUSTER_ID` | `${KAFKA_CLUSTER_ID}` | | | 클러스터 식별 UUID |

## Testing

```bash
# internal topic 목록 확인
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list

# schema registry 연결성 확인
docker inspect --format '{{json .State.Health}}' schema-registry
```

## Change Impact

- **브로커 설정 변경**: 순차적 재시작(Rolling Restart)이 필요하며, 가용성 보장을 위해 쿼럼 상태를 확인해야 한다.
- **토픽 정책 변경**: `replication.factor` 축소는 데이터 가용성을 낮추며, `retention` 변경은 디스크 용량에 즉각 영향을 준다.

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. **Initialize Topics**: 새 토픽은 반드시 `docker-compose.yml`의 `kafka-init` 서비스를 통해 관리되도록 설정한다.
2. **Monitor Health**: 브로커 점검 시 `UnderReplicatedPartitions` 지표가 0인지 항상 확인한다.
3. **SSoT Linkage**: 토픽 스펙 변경 시 `docs/03.specs/05-messaging/spec.md`를 함께 갱신한다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify topic creation by running `kafka-topics.sh --list` and confirming expected topics exist with correct partition and replication settings.
- Confirm producer/consumer connectivity by checking `docker logs kafka-1 --tail 100` after config changes.
- Verify broker registration by confirming the broker ID appears in the controller metadata logs.

## Troubleshooting

- Start with `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh` to confirm root-included messaging render.
- Service-local `docker compose -f infra/05-messaging/kafka/docker-compose.yml --profile messaging config` needs root `infra_net` and secret context or a validation overlay.
- Check Kafka logs and broker health before changing listener, storage, or KRaft settings.

## Related Documents

- **PRD**: [05-messaging](../../../docs/01.requirements/006-messaging.md)
- **ARD**: [Messaging Architecture](../../../docs/02.architecture/requirements/0005-messaging-architecture.md)
- **Guide**: [Kafka Guide](../../../docs/05.operations/guides/05-messaging/kafka.md)
- **Policy**: [Messaging Ops](../../../docs/05.operations/policies/05-messaging/kafka.md)
- **Runbook**: [Messaging Recovery](../../../docs/05.operations/runbooks/05-messaging/kafka.md)
