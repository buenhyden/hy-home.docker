# Messaging Operations Policy (05-messaging)

> Messaging Governance, Data Retention & Standard Procedures (05-messaging)

## Overview

이 문서는 `hy-home.docker` 메시징 Tier(05-messaging)의 운영 원칙과 메시지 데이터 관리 기준을 정의한다.

## Policy Goals

- **Reliability**: 메시지 전달 보장 및 중복 방지.
- **Consistency**: 스키마 레지스트리를 통한 데이터 정합성 유지.
- **Maintainability**: 표준화된 토픽 및 큐 명명 규칙 적용.

## Operational Standards

### 1. 데이터 보관 정책 (Retention)

- **Kafka Topics**: 
  - 기본 보관 기간(Retention Period): 7일.
  - 최대 크기(Retention Bytes): 토픽당 10GB.
  - 민감 데이터 토픽은 압축(Compact) 정책을 적용하지 않음.
- **RabbitMQ Queues**: 
  - 메시지 TTL(Time-To-Live) 설정을 통해 무한 대기 방지.
  - 처리 실패 메시지를 위한 Dead Letter Exchange(DLX) 필수 구성.

### 2. 스키마 관리 표준

- 모든 Kafka 메시지는 `Schema Registry`에 등록된 스키마를 따라야 한다.
- 호환성 정책은 `BACKWARD`를 기본으로 하며, 변경 시 소비자 영향도를 사전 평가해야 한다.

### 3. 모니터링 및 알람

- **Kafka**: `UnderReplicatedPartitions` 발생 시 즉시 조치.
- **RabbitMQ**: `Memory Alarm` 또는 `Disk Free Alarm` 발생 시 생산을 일시 중단하고 리소스를 확보함.

## Verification

- [ ] 분기별 메시지 처리 지연(Lag) 점검 및 소비자 스케일링 검토.
- [ ] 스키마 레지스트리 백업의 무결성 정기 확인.
- [ ] RabbitMQ 복구 절차 테스트 (HA 복제 확인).

## Related Documents

- **Setup Guides**: `[../../07.guides/05-messaging/README.md]`
- **Runbook**: `[../../09.runbooks/05-messaging/README.md]`
