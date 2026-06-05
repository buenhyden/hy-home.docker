---
status: active
---
<!-- Target: docs/05.operations/guides/05-messaging/kafka.md -->

# Kafka Usage Guide

## Usage

### Overview

이 문서는 `05-messaging` Kafka 사용 가이드다. 현재 root `docker-compose.yml`은 `infra/05-messaging/kafka/docker-compose.dev.yml`를 include해 단일 broker 개발 구성을 렌더링하고, `infra/05-messaging/kafka/docker-compose.yml`은 root network/secret context가 필요한 3 broker full compose로 유지한다.

### Usage Type

`system-guide | how-to | operational-reference`

### Target Audience

- Developers
- Operators
- Data Engineers
- AI Agents

### Purpose

이 가이드는 Kafka deployment surface, topic 작업 경계, Schema Registry/Kafka Connect 접근 경로, 일반 점검 방법을 설명한다.

### Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- Repository root에서 실행 가능한 `docker compose`
- [infra/05-messaging/kafka README](../../../../infra/05-messaging/kafka/README.md)
- Full 3 broker compose를 service-local로 검증하려면 root `infra_net` 및 `kafbat_client_secret` context 또는 임시 validation overlay가 필요하다.

### Step-by-step Instructions

1. Deployment surface를 확인한다.

```bash
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
docker compose --env-file .env.example --profile messaging config --services
```

현재 root messaging profile은 `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`, `rabbitmq`를 렌더링한다.

1. Kafka topic 작업은 실행 중인 broker 컨테이너 내부 CLI로 수행한다.

```bash
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --topic infra-events
```

Full 3 broker compose에서는 `replication-factor=3` 토픽을 사용할 수 있다. Root-included dev compose는 단일 broker이므로 신규 토픽에 `replication-factor=3`을 요구하지 않는다.

1. Schema Registry와 Kafka Connect는 내부 service DNS 또는 Traefik route로 확인한다.

```bash
docker inspect --format '{{json .State.Health}}' schema-registry
docker inspect --format '{{json .State.Health}}' kafka-connect
```

- Internal endpoints: `http://schema-registry:8081`, `http://kafka-connect:8083`, `http://kafka-rest-proxy:8082`
- Gateway routes: `https://schema-registry.${DEFAULT_URL}`, `https://kafka-connect.${DEFAULT_URL}`, `https://kafka-rest.${DEFAULT_URL}`
- Kafbat UI route: `https://kafbat-ui.${DEFAULT_URL}` with `gateway-standard-chain@file,sso-errors@file,sso-auth@file`

1. Kafka Connect connector 등록/변경은 정책 검토 후 수행한다.
   - connector secret 값은 문서나 shell history에 남기지 않는다.
   - Connector runtime state는 `kafka-connect` health와 logs를 함께 확인한다.

### Common Pitfalls

- root-included dev compose를 3 broker HA 구성으로 오해하는 경우
- service-local compose를 root network/secret context 없이 standalone으로 검증하려는 경우
- dev single broker에서 `replication-factor=3` 토픽을 생성하려는 경우
- compose에 선언되지 않은 전역 retention 값을 current truth로 단정하는 경우

## Common Checks

- `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 05-messaging`
- `docker exec kafka-1 kafka-broker-api-versions --bootstrap-server localhost:19092`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/05-messaging/kafka.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/05-messaging/kafka.md)
- [Recovery runbook](../../runbooks/05-messaging/kafka.md)
- [Infra README](../../../../infra/05-messaging/kafka/README.md)
