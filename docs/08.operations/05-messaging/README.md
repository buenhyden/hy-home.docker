# Messaging Operations Policy (05-messaging)

> Messaging Governance, Data Retention & Standard Procedures.

## Overview (KR)

이 문서는 `hy-home.docker` 메시징 티어(05-messaging)의 운영 원칙과 데이터 관리 기준을 정의한다. 시스템 가용성 보장과 데이터 정합성을 위한 SSoT(Single Source of Truth) 정책을 다룬다.

## Reliability Standards

- **Quorum Requirement**: Kafka/RabbitMQ 클러스터는 항상 과반수(Quorum) 이상의 노드가 활성 상태여야 한다.
- **Backpressure Policy**: 소비자의 처리 속도가 생산량을 따라가지 못할 경우, 생산자 속도 제한(Throttling)을 적용한다.

## Operational Standards

### 1. 데이터 보관 정책 (Retention)
- **Kafka Topics**: 
  - 기본 보관: `retention.ms=604800000` (7일).
  - 최대 크기: `retention.bytes=10737418240` (10GB/Partition).
- **RabbitMQ Queues**: 
  - 메시지 TTL 설정 권장 (무한 대기 방지).
  - `Dead Letter Exchange(DLX)` 필수 구성을 통한 처리 실패 메시지 격리.

### 2. 스키마 거버넌스
- 모든 Kafka 메시지는 `Schema Registry`를 통해 검증되어야 한다.
- **Compatibility**: `BACKWARD`를 기본으로 하며, 변경 시 소비자 영향도를 사전 평가한다.

### 3. 모니터링 임계치
- **Kafka**: `UnderReplicatedPartitions` > 0 발생 시 즉시 점검.
- **RabbitMQ**: `Memory Alarm` 발생 시 생산 중단 자동화 연동.

## Verification Procedures

- [ ] 분기별 메시지 처리 지연(Lag) 통계 분석 및 하드웨어 리소스 최적화.
- [ ] 스키마 레지스트리 백업 본의 정기 복구 테스트.
- [ ] 비정상 노드 탈퇴 시 쿼럼 유지 여부 시뮬레이션.

## Traceability

- **PRD**: [2026-03-26-05-messaging.md](../../01.prd/2026-03-26-05-messaging.md)
- **ARD**: [0005-messaging-architecture.md](../../02.ard/0005-messaging-architecture.md)
- **Guide**: [Messaging Guide](../../07.guides/05-messaging/README.md)
- **Runbook**: [Messaging Runbook](../../09.runbooks/05-messaging/README.md)
