---
status: active
---
<!-- Target: docs/05.operations/policies/05-messaging/rabbitmq.md -->

# RabbitMQ Operations Policy

> Scope: Operational standards for RabbitMQ message broker.

---

## Overview

이 문서는 `05-messaging` RabbitMQ 서비스의 운영 정책을 정의한다. Docker Secrets 기반 인증, AMQP/Management 경계, queue mutation 승인, 정적 검증 기준을 규정한다.

## Policy Scope

이 정책은 `infra/05-messaging/rabbitmq/docker-compose.yml`의 `rabbitmq` service, `rabbitmq_user`/`rabbitmq_password` Docker Secrets, AMQP host port, Management UI route, linked guide/runbook에 적용한다.

## Controls

- **Required**:
  - `rabbitmq_user` 및 `rabbitmq_password`는 Docker Secrets로만 주입한다.
  - Management UI route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware를 유지한다.
  - AMQP 데이터 평면은 host port mapping 또는 `infra_net` 내부 endpoint를 사용하고, Traefik HTTP route를 AMQP endpoint로 문서화하지 않는다.
  - Queue purge/delete/rebind 같은 데이터 영향 작업은 승인과 evidence 없이 실행하지 않는다.
- **Allowed**:
  - `messaging` 및 `messaging-option` profile을 통한 활성화
  - Runtime-approved definition export/import 절차를 별도 task 또는 incident evidence에 기록한 뒤 실행
  - 서비스별 VHost/permission 분리는 최소 권한 검토 후 적용
- **Disallowed**:
  - secret 값, credential dump, token, 인증서 원문 기록
  - 미검증 backup/restore 명령을 current runbook 절차로 승격
  - 메시지 손실 가능 조치를 일반 troubleshooting 단계로 실행

## Exceptions

- 긴급 장애 대응 중 데이터 영향 조치가 필요하면 Messaging Operator 승인, 영향 queue, 예상 손실, 실행자, 검증 결과를 incident/task evidence에 기록한다.

## Verification

- `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 05-messaging`
- `docker exec rabbitmq rabbitmq-diagnostics -q check_running`
- `docker exec rabbitmq rabbitmqctl list_queues name messages consumers`
- `bash scripts/validation/check-doc-traceability.sh` when execution or operations links change.

## Review Cadence

- Quarterly 또는 RabbitMQ compose, secrets, route, queue mutation policy 변경 시 검토.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/05-messaging/rabbitmq.md)
- [Recovery runbook](../../runbooks/05-messaging/rabbitmq.md)
