# RabbitMQ Recovery Runbook (05-messaging)

> Step-by-step procedures for broker recovery, maintenance, and troubleshooting.

## Overview (KR)

이 문서는 RabbitMQ 서비스 장애 시 신속한 복구를 위한 실행 절차를 제공한다. 브로커 프로세스 복구, 메시지 폭주 대응(Purge), 그리고 성능 최적화(Rebalance) 절차를 포함한다.

## Traceability (Golden 5)

- **PRD**: [05-messaging (2026-03-26)](../../01.prd/2026-03-26-05-messaging.md)
- **ARD**: [Messaging Architecture (0005)](../../02.ard/0005-messaging-architecture.md)
- **Spec**: [Messaging Specification](../../04.specs/05-messaging/spec.md)
- **Operation**: [RabbitMQ Operation Policy](../../08.operations/05-messaging/rabbitmq.md)

## Recovery Procedures

### 1. Broker Process Recovery

브로커가 응답하지 않거나 중단된 경우:

```bash
# 1. Container status check
docker ps -f name=rabbitmq

# 2. Restart service
cd infra/05-messaging/rabbitmq
docker compose restart rabbitmq

# 3. Verify health
docker exec rabbitmq rabbitmq-diagnostics check_running
```

### 2. High Queue Depth / Message Spike

특정 큐에 메시지가 수만 건 이상 쌓여 시스템이 느려진 경우:

```bash
# 1. Identify problematic queue
docker exec rabbitmq rabbitmqctl list_queues name messages_ready

# 2. Purge messages (CAUTION: Data Loss)
docker exec rabbitmq rabbitmqctl purge_queue <queue_name>
```

### 3. Blocked Producers

메모리/디스크 임계치 초과로 생산이 중단된 경우:

1. `rabbitmq-diagnostics status` 명령으로 원인이 `Memory`인지 `Disk`인지 확인한다.
2. 디스크 부족 시 `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq` 경로의 로그 또는 오래된 데이터를 정리한다.

## Performance Troubleshooting

### Consumer Lag
소비자 처리 속도가 느린 경우:
1. `rabbitmqctl list_consumers`를 통해 활성 소비자 수를 확인한다.
2. 소비자 파드(Pod)의 스케일아웃(Scale-out)을 수행한다.
3. Prefetch Count 설정을 조정하여 처리 효율을 높인다.

## Maintenance Operations

### Credential Rotation
비밀번호 변경 시:
1. Vault 또는 `.env` 파일의 `RABBITMQ_PASSWORD`를 업데이트한다.
2. 컨테이너를 재시작하여 새로운 비밀번호를 적용한다.
3. 기존 연결(Connection)을 강제 종료하여 재인증을 유도한다.
