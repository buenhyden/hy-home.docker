---
title: "Kafka 메시징"
version: "1.3.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

# Kafka

## Purpose

### Service Role

이 패키지는 저장소의 Kafka 계열 메시징 surface를 정의합니다.

#### Audience

Kafka와 그 companion 서비스들의 operator 및 maintainer를 대상으로 합니다.

[`docker-compose.yml`](docker-compose.yml)은 정상 단일 `kafka-1`,
`kafbat-ui`, `kafka-exporter`, `kafka-init`을 정의합니다. 정상 selector는
`messaging`, `messaging-broker`, `messaging-admin`입니다.

Schema Registry와 Debezium Connect는 2026-11-10 owner 결정(ADR-0062 개정)으로 HOME에서
[`labs/kafka-cluster`](../../../labs/kafka-cluster/README.md) LAB으로 옮겼습니다(HOME에서 connector 0개,
subject 0개, CDC 원천 DB `platform_dev` 없음). `debezium-db-provision`, 커넥터 샘플, 기능 SQL과 secret
renderer는 제거했고 Git 이력이 보존합니다. Kafbat은 schema registry와 Connect cluster를 설정하지 않습니다.

#### Structure

정상 broker 상태는 `${DEFAULT_MESSAGE_BROKER_DIR}/kafka` 아래의 별도
bind 기반 volume을 사용합니다. 서비스들은 `kafka_net`에 참여합니다. 라우팅되는
Kafbat UI는 `edge_net`에 참여합니다. Broker, controller, 게시된 broker/JMX
listener는 PLAINTEXT이며 broker TLS/클라이언트 인증은 선언되어 있지
않습니다. Kafbat HTTP 포트는 내부용으로 유지되며 라우트는 Traefik을 사용합니다.
Broker, Kafbat, exporter는 각 역할에 맞는 healthcheck를 선언하고
init은 one-shot job입니다.
[`jmx-exporter/kafka_broker.yml`](jmx-exporter/kafka_broker.yml)(Confluent 규칙, SPEC-0193)과 OIDC
템플릿이 마운트되는 설정 소스입니다.

Kafbat은 [`kafbat-ui/dynamic_config.template.yaml`](kafbat-ui/dynamic_config.template.yaml)을
tmpfs로 렌더링하고 `kafbat_client_secret`을 읽으며 로컬 CA를 신뢰하고
네이티브 Keycloak OIDC와 `/admins`, `/users` RBAC을 사용합니다. 이 서비스의
Traefik 라우트는 `gateway-standard-chain@file`을 사용하며 forwarding-auth
체인은 이 라우트에 속하지 않습니다.

### Supported Environment

정상 Kafka 단일 브로커와 Kafbat·exporter 등의 이미지 선언은 [Compose](docker-compose.yml)가 소유합니다. Connect 이미지 빌드는 LAB의 [Dockerfile](../../../labs/kafka-cluster/connect/Dockerfile)이 소유합니다.

## Interfaces

### Inputs and Outputs

정상 `kafka_net`의 secret, 라우트, 포트 및 healthcheck 계약은 위 구조와 Compose에 따릅니다.

### Security Boundary

Compose가 참조하는 secret은 `kafbat_client_secret`이며 값은 저장소에 두지 않는다. 호스트로 게시되는 포트는 `127.0.0.1:${KAFKA_EXTERNAL_1_HOST_PORT:-9092}:${KAFKA_EXTERNAL_PORT:-9092}`, `127.0.0.1:${KAFKA_JMX_EXPORTER_1_HOST_PORT:-19404}:${KAFKA_JMX_EXPORTER_PORT:-9404}`이다. (출처: `infra/05-messaging/kafka/docker-compose.yml`의 `kafka-1`, `kafbat-ui`, `kafka-exporter`, `kafka-init` 서비스)

## Development

### Local Workflow

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
```

정상 `kafka-init`은 복제 계수 1로 토픽을 만듭니다. 위 명령은 정적 render이며
서비스와 topic을 시작·생성하지 않습니다.

복구에는 토픽 record/config, 파티션, consumer offset, KRaft metadata가
포함되어야 합니다. 승인된
replay/replication을 통해 새로운 격리된 클러스터로 복원해야 하며 기존
KRaft identity나 개별 broker 디렉터리를 그대로 재사용해서는 안 됩니다.

### Checks

아래 명령으로 정상 구성을 렌더합니다. 렌더 성공은 브로커 복구 성공을 증명하지 않습니다.

## Operations

### Runbook Links

#### Related Documents

[문서 진입점](../../../docs/README.md)을 사용해 Stage 05 subject
`docs/05.operations/guides/06-messaging-and-cdc/0036-kafka.md`와 hardening subject
`docs/05.operations/guides/06-messaging-and-cdc/0037-messaging-optimization-hardening.md`을
찾으십시오. 공식 문서: [Kafka operations](https://kafka.apache.org/documentation/#operations),
[Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html),
[Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control).

### Observability and Recovery

헬스체크: `kafka-1` 서비스는 `unset KAFKA_OPTS; kafka-broker-api-versions --bootstrap-server localhost:${KAFKA_INTERNAL_PORT:-19092} >/dev/null || exit 1` (interval 60s); `kafbat-ui` 서비스는 `wget --no-verbose --tries=1 --spider http://localhost:${KAFKA_UI_PORT:-8080}/actuator/health` (interval 15s); `kafka-exporter` 서비스는 `wget --quiet --tries=1 --spider http://localhost:${KAFKA_EXPORTER_PORT:-9308}/metrics || exit 1` (interval 15s).
