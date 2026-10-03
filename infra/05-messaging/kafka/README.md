---
title: "Kafka Messaging"
version: "1.2.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
created: "2025-11-12"
---

# Kafka

## Overview

이 패키지는 저장소의 Kafka 계열 메시징 surface를 정의합니다.

## Audience

Kafka와 그 companion 서비스들의 operator 및 maintainer를 대상으로 합니다.

## Scope

[`docker-compose.yml`](docker-compose.yml)은 정상 단일 `kafka-1`,
`schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`,
`kafka-exporter`, `kafka-init`, `debezium-db-provision`을 정의합니다. 정상
selector는 `messaging`, `messaging-broker`, `messaging-schema`,
`messaging-connect`, `messaging-rest`, `messaging-admin`, `cdc`입니다.
[`labs/kafka-cluster.yml`](../../../labs/kafka-cluster.yml)은 독립된
`lab-kafka` 프로파일의 브로커 3개, exporter와 init job을 정의합니다.
정상 root는 LAB 파일을 include하지 않으며 LAB는 독립 Compose project입니다.

Connect는 Debezium PostgreSQL 플러그인을 사용해
[`Dockerfile.connect`](Dockerfile.connect)로부터 빌드됩니다.
[`connect/render-connect-secrets.sh`](connect/render-connect-secrets.sh)는
시작할 때마다 `debezium_postgres_password` secret으로부터
`FileConfigProvider` 입력을 렌더링하며 `allowed.paths`로 범위가 제한됩니다.
커넥터 정의([`postgres-connector.json`](connect/debezium/postgres-connector.json))와
기능 SQL([`provisioning/dev-pg.sql`](connect/debezium/provisioning/dev-pg.sql))은
`connect/debezium/` 아래에 있으며 이 JSON은 자동으로 등록되지 않습니다.

## Structure

정상 broker와 Connect 상태는 `${DEFAULT_MESSAGE_BROKER_DIR}/kafka` 아래의 별도
bind 기반 volume을 사용합니다. LAB 브로커는 `${LAB_DATA_DIR}/kafka`의
별도 디렉터리와 LAB 전용 network·cluster ID를 사용하며 정상 offset과
상태를 공유하지 않습니다. 서비스들은 `kafka_net`에 참여하고 라우팅되는
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
docker compose --env-file .env.example -f labs/kafka-cluster.yml --profile lab-kafka config --quiet
```

정상 `kafka-init`은 복제 계수 1로 토픽을 만들고, LAB
`lab-kafka-init`은 독립된 세 브로커에 복제 계수 3으로 LAB 토픽을 만듭니다.
`LAB_KAFKA_CLUSTER_ID`는 정상 `KAFKA_CLUSTER_ID`와 다른 유효한 KRaft ID여야
합니다. 이 명령은 정적 render이며 서비스와 topic을 시작·생성하지 않습니다.

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
