---
status: active
---
<!-- Target: docs/05.operations/guides/05-messaging/rabbitmq.md -->

# RabbitMQ Usage Guide

## Usage

### Overview (KR)

이 문서는 `05-messaging` RabbitMQ 사용 가이드다. AMQP 데이터 평면, Management UI 접근 경계, Docker Secrets 기반 인증 주입, 일반 점검 방법을 설명한다.

### Usage Type

`system-guide`

### Target Audience

- Backend Developer
- SRE

### Purpose

- RabbitMQ 서비스 연결 및 인증 설정
- Management UI 사용법 및 모니터링
- 큐(Queue) 및 익스체인지(Exchange) 설계 가이드

### Prerequisites

- Repository root에서 `messaging` profile을 렌더링할 수 있어야 함.
- AMQP 클라이언트 라이브러리(pika, amqplib 등)
- RabbitMQ credential 값은 `rabbitmq_user`, `rabbitmq_password` Docker Secrets에서 런타임에 주입되며 문서에 기록하지 않는다.

### Step-by-step Instructions

#### 1. 연결 정보 및 인증 경계

- **Host AMQP port**: `${RABBITMQ_HOST_PORT:-5672}` -> container `${RABBITMQ_PORT:-5672}`
- **Management Console**: `https://rabbitmq.${DEFAULT_URL}`
- **Internal AMQP endpoint**: `rabbitmq:5672`
- **Credential source**: `/run/secrets/rabbitmq_user`, `/run/secrets/rabbitmq_password`

Traefik route는 Management UI HTTP 경로를 대상으로 한다. AMQP 프로토콜은 Traefik HTTP route가 아니라 host port mapping 또는 `infra_net` 내부 endpoint를 사용한다.

#### 2. Management UI 접속

웹 브라우저에서 `https://rabbitmq.${DEFAULT_URL}`에 접속하여 브로커 상태를 모니터링할 수 있다. 이 경로는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware를 사용한다.

- **Connections**: 활성 클라이언트 연결 확인
- **Channels**: 활성 채널 및 처리량 확인
- **Exchanges**: 메시지 라우팅 규칙 설정
- **Queues**: 대기 중인 메시지 수 및 소비자 상태 확인

#### 3. 주요 설정 가이드

- **VHost**: 기본 VHost는 `/`를 사용하며, 서비스별로 분리 시 별도의 VHost 생성을 권장한다.
- **Quorum Queues**: 데이터 일관성이 중요한 경우 일반 큐 대신 Quorum 큐를 사용한다.
- **Message Durability**: 서비스 재시작 시에도 메시지를 보존하려면 `durable: true` 설정을 활성화해야 한다.

#### 4. 클라이언트 연동 예시 (Python/pika)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
connection.close()
```

### Common Pitfalls

- **Protocol mix-up**: `https://rabbitmq.${DEFAULT_URL}`는 Management UI 경로이며 AMQP endpoint가 아니다.
- **Credential handling**: secret 파일 값을 문서, 로그, task evidence에 기록하지 않는다.
- **Queue mutation**: purge/delete/rebind는 메시지 손실 가능성이 있으므로 runbook escalation 기준을 따른다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
- `docker exec rabbitmq rabbitmq-diagnostics -q check_running`
- `docker exec rabbitmq rabbitmqctl list_queues name messages consumers`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/05-messaging/rabbitmq.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/05-messaging/rabbitmq.md)
- [Recovery runbook](../../runbooks/05-messaging/rabbitmq.md)
- [Infra README](../../../../infra/05-messaging/rabbitmq/README.md)
