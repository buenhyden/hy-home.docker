---
title: "Kafka Messaging"
version: "1.2.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-30"
created: "2025-11-12"
---

# Kafka

## Overview

이 패키지는 저장소의 Kafka 계열 메시징 surface를 정의합니다.

## Audience

Kafka와 그 companion 서비스들의 operator 및 maintainer를 대상으로 합니다.

## Scope

[`docker-compose.yml`](docker-compose.yml)은 `kafka-1`, `kafka-2`,
`kafka-3`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`,
`kafka-exporter`, `kafka-init`, `debezium-db-provision`을 정의합니다. 루트
selector에는 `messaging`, `messaging-broker`, `messaging-cluster`,
`messaging-schema`, `messaging-connect`, `messaging-rest`, `messaging-admin`,
`cdc`가 있으며 broker 2와 3은 `messaging-cluster`에만 속합니다. `cdc`는
broker, Schema Registry, Connect, CDC source provisioning job을 선택합니다.

Connect는 Debezium PostgreSQL 플러그인을 사용해
[`Dockerfile.connect`](Dockerfile.connect)로부터 빌드됩니다.
[`connect/render-connect-secrets.sh`](connect/render-connect-secrets.sh)는
시작할 때마다 `debezium_postgres_password` secret으로부터
`FileConfigProvider` 입력을 렌더링하며 `allowed.paths`로 범위가 제한됩니다.
커넥터 정의([`postgres-connector.json`](connect/debezium/postgres-connector.json))와
기능 SQL([`provisioning/mng-pg.sql`](connect/debezium/provisioning/mng-pg.sql))은
`connect/debezium/` 아래에 있으며 이 JSON은 자동으로 등록되지 않습니다.

## Structure

Broker와 Connect 상태는 `${DEFAULT_MESSAGE_BROKER_DIR}/kafka` 아래의 별도
bind 기반 volume을 사용합니다. 서비스들은 `kafka_net`에 참여하고 라우팅되는
서비스는 `edge_net`에도 참여합니다. Broker, controller, 게시된 broker/JMX
listener는 PLAINTEXT이며 broker TLS/클라이언트 인증은 선언되어 있지
않습니다. Schema Registry, Connect, REST, Kafbat HTTP 포트는 내부용으로
유지되며 일부 라우트는 Traefik을 사용합니다. Broker, Schema Registry,
Connect, REST, Kafbat, exporter는 각 역할에 맞는 healthcheck를 선언하고
init은 one-shot job입니다.
[`jmx-exporter/kafka_broker.yml`](jmx-exporter/kafka_broker.yml)(Confluent 규칙, SPEC-0193)과 OIDC
템플릿이 마운트되는 설정 소스입니다.

Kafbat은 [`kafbat-ui/dynamic_config.template.yaml`](kafbat-ui/dynamic_config.template.yaml)을
tmpfs로 렌더링하고 `kafbat_client_secret`을 읽으며 로컬 CA를 신뢰하고
네이티브 Keycloak OIDC와 `/admins`, `/users` RBAC을 사용합니다. 이 서비스의
Traefik 라우트는 `gateway-standard-chain@file`을 사용하며 forwarding-auth
체인은 이 라우트에 속하지 않습니다.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
docker compose --env-file .env.example --profile messaging-cluster config --quiet
```

Init job은 복제 계수(replication factor) 3으로 토픽 2개를 생성하므로 정상적인
bootstrap을 위해서는 건강한 broker 3개가 필요합니다. 단일 broker
`messaging` selector로 초기화가 완료될 수 있다고 가정하지 마십시오.

복구에는 토픽 record/config, 파티션, consumer offset, KRaft metadata, Schema
Registry 이력/ID, Connect 정의, 내부 상태가 포함되어야 합니다. 승인된
replay/replication을 통해 새로운 격리된 클러스터로 복원해야 하며 기존
KRaft identity나 개별 broker 디렉터리를 그대로 재사용해서는 안 됩니다.

## Related Documents

[문서 진입점](../../../docs/README.md)을 사용해 Stage 05 subject
`docs/05.operations/guides/0036-kafka.md`와 hardening subject
`docs/05.operations/guides/0037-messaging-optimization-hardening.md`을
찾으십시오. 공식 문서: [Kafka operations](https://kafka.apache.org/documentation/#operations),
[Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html),
[Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control).
