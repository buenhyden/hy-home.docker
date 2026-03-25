# Messaging Runbook (05-messaging)

> Messaging Infrastructure Recovery & Incident Response (05-messaging)

## Overview

이 런북은 `hy-home.docker`의 메시징 인프라(05-messaging)에서 발생할 수 있는 주요 장애 상황과 복구 절차를 정의한다.

## Purpose

메시지 유실을 방지하고, 브로커 및 스트리밍 서비스의 가용성을 급속히 복구하기 위함이다.

---

## Recovery Procedures

### 1. Kafka 브로커 복구 및 리더 재선출

브로커 노드 다운으로 인해 특정 파티션의 리더가 없는 경우.

1. **상태 확인**: `kafbat-ui` 또는 CLI 확인.
   ```bash
   docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --under-replicated-partitions
   ```
2. **서비스 재시작**: 문제가 있는 컨테이너를 재시작하여 쿼럼 재합류 유도.
3. **리더 밸런싱**: 필요한 경우 수동으로 리더 최적화 실행.

### 2. Schema Registry 연동 오류 해결

데이터 생산자가 스키마를 읽거나 쓰지 못하는 경우.

1. **연결성 확인**: `schema-registry` 서비스 상태 확인.
2. **데이터 클린업 (주의)**: 스키마 레지스트리 저장 토픽(`_schemas`)의 데이터가 깨진 경우, 스키마 레지스트리 백업으로부터 복원을 검토한다.

### 3. RabbitMQ 메시지 폭주 대응 (Backpressure)

컨슈머 처리 속도보다 메시지 인입 속도가 훨씬 빠른 경우.

1. **소비자 스케일 아웃**: 해당 큐를 구독하는 컨슈머 컨테이너 수를 늘린다.
2. **임시 퍼지(Purge)**: 비정상적으로 생성된 대량의 무의미한 메시지가 쌓인 경우, 관리 UI에서 해당 큐를 `Purge` 한다 (데이터 유실 주의).

---

## Maintenance Tasks

- **Log Cleaner 점검**: Kafka 로그 세그먼트가 설정된 기간에 맞춰 삭제되는지 점검.
- **RabbitMQ Version Upgrade**: 클러스터 상태를 유지하며 순차적(Rolling) 업데이트 수행.

## Verification Steps

- [ ] `kafka-broker-api-versions` 성공 응답 확인.
- [ ] `rabbitmqctl list_queues`로 정상 처리 상태 확인.

## Related Operational Documents

- **Operations Policy**: `[../../08.operations/05-messaging/README.md]`
- **Kafka Guide**: `[../../07.guides/05-messaging/01.kafka-kraft.md]`
