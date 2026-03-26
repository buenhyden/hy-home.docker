# Messaging Runbook (05-messaging)

> Messaging Infrastructure Recovery & Incident Response.

## Overview (KR)

이 런북은 `hy-home.docker`의 메시징 인프라(05-messaging)에서 발생할 수 있는 주요 장애 상황과 복구 절차를 정의한다. 데이터 손실 최소화와 신속한 서비스 가동을 최우선 목표로 한다.

## Incident Response Priorities

1. **Service Resumption**: 브로커 쿼럼 복구 및 클라이언트 연결 재개.
2. **Data Consistency**: 스키마 오류 해결 및 누락된 데이터 재처리.
3. **Performance Recovery**: 백래그(Back-log) 해소 및 소비자 스케일 아웃.

## Recovery Procedures

### 1. Kafka Cluster Quorum Failure
- **Symptom**: `No Leader found` 에러 및 생산/소비 중단.
- **Action**:
  1. 문제가 발생한 노드의 컨테이너 로그에서 `Fatal Error` 확인.
  2. 서비스 재시작: `docker compose restart kafka-X`.
  3. 상태 확인: `docker exec kafka-1 kafka-topics --bootstrap-server localhost:19092 --describe --under-replicated-partitions`.

### 2. Schema Registry Sync Error
- **Symptom**: 생산자가 스키마를 유효화하지 못해 전송 실패.
- **Action**:
  1. `schema-registry` 서비스와 브로커 간의 연결 확인.
  2. 레지스트리 재시작 후 메타데이터 토픽(`_schemas`)의 리더가 정상인지 확인.

### 3. RabbitMQ Message Spike (Backpressure)
- **Symptom**: 처리되지 않은 메시지가 큐에 쌓여 메모리 경고 발생.
- **Action**:
  1. **Scale-Out**: 해당 큐를 구독하는 소비자 컨테이너를 증설한다.
  2. **Temporary Purge**: 테스트나 루프에 의한 무의미한 대량 메시지인 경우 관리 UI에서 `Purge` 한다 (주의: 데이터 실 가용성 확인).

## Maintenance Tasks

- **Log Cleanup**: Kafka 로그 세그먼트 정책 작동 여부 정기 점검.
- **Version Upgrades**: 순차적(Rolling) 업데이트를 통해 서비스 중단 없이 최신 패치 적용.

## Related Documents

- **Operations Policy**: [../../08.operations/05-messaging/README.md]
- **Messaging Guide**: [../../07.guides/05-messaging/README.md]
- **Infrastructure Source**: [../../../infra/05-messaging/README.md]
