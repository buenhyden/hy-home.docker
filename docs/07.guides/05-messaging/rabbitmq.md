# RabbitMQ Service Guide

> Standardized AMQP message broker for task queuing and asynchronous messaging.

---

## Overview (KR)

이 문서는 RabbitMQ 메시지 브로커에 대한 기술 가이드를 제공한다. `hy-home.docker` 환경에서 RabbitMQ를 연동하고 관리하는 방법, 큐 관리 정책 및 메시지 안정성 확보 방안을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- Backend Developer
- SRE

## Purpose

- RabbitMQ 서비스 연결 및 인증 설정
- Management UI 사용법 및 모니터링
- 큐(Queue) 및 익스체인지(Exchange) 설계 가이드

## Prerequisites

- `infra/05-messaging/rabbitmq` 서비스가 실행 중이어야 함.
- AMQP 클라이언트 라이브러리 (pika, amqplib 등) 설치.

## Step-by-step Instructions

### 1. 연결 정보 및 인증

- **Endpoint (External)**: `amqp://rabbitmq.${DEFAULT_URL}:5672`
- **Management Console**: `https://rabbitmq.${DEFAULT_URL}`
- **Internal API**: `rabbitmq:5672`
- **Username/Password**: `rabbitmq_user` 및 `rabbitmq_password` 시크릿 파일에서 주입됨.

### 2. Management UI 접속

웹 브라우저에서 `https://rabbitmq.${DEFAULT_URL}`에 접속하여 브로커 상태를 모니터링할 수 있다.

- **Connections**: 활성 클라이언트 연결 확인
- **Channels**: 활성 채널 및 처리량 확인
- **Exchanges**: 메시지 라우팅 규칙 설정
- **Queues**: 대기 중인 메시지 수 및 소비자 상태 확인

### 3. 주요 설정 가이드

- **VHost**: 기본 VHost는 `/`를 사용하며, 서비스별로 분리 시 별도의 VHost 생성을 권장한다.
- **Quorum Queues**: 데이터 일관성이 중요한 경우 일반 큐 대신 Quorum 큐를 사용한다.
- **Message Durability**: 서비스 재시작 시에도 메시지를 보존하려면 `durable: true` 설정을 활성화해야 한다.

### 4. 클라이언트 연동 예시 (Python/pika)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
connection.close()
```

## Common Pitfalls

- **Default Credentials**: `guest/guest`는 보안상 비활성화되어 있다. 반드시 Vault/Secrets를 통해 생성된 계정을 사용해야 한다.
- **OOM Kill**: RabbitMQ는 메모리 사용량이 임계치에 도달하면 메시지 수신을 차단한다. 모니터링 대시보드에서 `Memory Workflow`를 상시 확인해야 한다.

## Related Documents

- **Operation**: `[../08.operations/05-messaging/rabbitmq.md]`
- **Runbook**: `[../09.runbooks/05-messaging/rabbitmq.md]`
