---
status: active
---
<!-- Target: docs/05.operations/policies/05-messaging/kafka.md -->

# Kafka Operations Policy

> Governance, topic safety, secret boundary, and reliability standards for Kafka.

## Overview (KR)

이 문서는 `05-messaging` Kafka 운영 정책을 정의한다. Root-included dev Kafka, service-local full Kafka compose, Schema Registry, Kafka Connect, Kafka REST Proxy, Kafbat UI, Kafka Exporter에 대한 필수 통제 기준을 포함한다.

## Policy Scope

이 정책은 Kafka broker, Schema Registry, Kafka Connect, Kafka REST Proxy, Kafbat UI, Kafka Exporter와 Kafka topic 변경 절차를 제어한다.

- **Systems**: root dev Kafka single broker, service-local full Kafka 3 broker compose, Schema Registry, Kafka Connect, Kafka REST Proxy, Kafbat UI, Kafka Exporter
- **Agents**: AI Infrastructure Agent, CI/CD Deployer
- **Environments**: Local, Development, Production-like validation

## Controls

- **Required**:
  - Root-included messaging compose는 `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`를 통과해야 한다.
  - Kafka 관리 route는 `gateway-standard-chain@file`를 유지하고 Kafbat UI route는 `sso-errors@file,sso-auth@file`를 포함해야 한다.
  - Kafbat UI OAuth client secret은 `kafbat_client_secret` Docker Secret으로만 주입한다.
  - `kafka-init`가 선언한 `infra-events`, `application-logs` 토픽 변경은 compose diff와 검증 evidence를 남긴다.
  - Full 3 broker compose에서 production-like 토픽을 추가할 때는 replication factor와 ISR 기준을 정책 검토 evidence에 명시한다.
- **Allowed**:
  - Root-included dev compose의 단일 broker 토픽은 development-only로 `replication-factor=1`을 사용할 수 있다.
  - Schema Registry compatibility 변경은 영향 범위, consumer 호환성, rollback/escalation 기준이 task evidence에 기록된 경우 허용한다.
- **Disallowed**:
  - 현재 compose에 선언되지 않은 전역 `retention.ms` 값을 current truth로 문서화하는 것
  - secret 값을 문서, 로그, task evidence, PR 본문에 기록하는 것
  - delete topic, partition reassignment, retention 축소 같은 데이터 영향 작업을 승인/evidence 없이 실행하는 것

## Exceptions

- 단기 성능 테스트용 토픽 또는 dev-only topic은 owner, 만료 기준, cleanup 책임을 task evidence에 기록한 경우 예외로 허용한다.
- 데이터 손실 가능성이 있는 topic mutation은 Messaging Operator 승인과 incident/task evidence가 필요하다.

## Verification

- `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 05-messaging`
- `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --list`
- `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --under-replicated-partitions`

## Review Cadence

- Quarterly 또는 Kafka compose, topic policy, Schema Registry, Kafbat UI route 변경 시 검토.

## AI Agent Policy Section

- **Automated Topic Creation**: 자동 생성은 `kafka-init` compose 선언 또는 승인된 task evidence로만 허용한다.
- **Health Guardrails**: 복제 오류 발생 시 AI Agent는 destructive topic mutation을 수행하지 않고 runbook evidence capture와 escalation을 우선한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/05-messaging/kafka.md)
- [Recovery runbook](../../runbooks/05-messaging/kafka.md)
