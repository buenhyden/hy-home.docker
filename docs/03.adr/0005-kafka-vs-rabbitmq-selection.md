# ADR-0005: Polyglot Messaging Strategy (Kafka & RabbitMQ Selection)

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼에서 Apache Kafka와 RabbitMQ를 모두 채택한 폴리글랏 메시징 전략에 대한 의사 결정 기록이다. 스트리밍 데이터와 비동기 태스크 큐의 서로 다른 요구사항을 충족하기 위한 선택이다.

## Context

현대적인 마이크로서비스 아키텍처는 두 가지 유형의 메시징 패턴이 혼재되어 상호작용한다:
1. **고처리량 이벤트 스트리밍**: 로그 수집, 실시간 분석, 데이터 복제 등 대용량 데이터 전송.
2. **비동기 작업 큐**: 작업 분배, 푸시 알림, 지연 실행 등 단발성 메시지 전달.

단일 솔루션(Kafka 또는 RabbitMQ)으로 이 두 요구사항을 모두 충족하려 할 경우 운영 복잡성이 높고 효율성이 떨어지므로, 각 도구의 강점을 극대화하는 방식이 필요하다.

## Decision

- **Apache Kafka**를 **Primary Event Backbone**으로 선정한다.
  - 대량 로그 수집 및 영구 이벤트 스트림 보관용.
  - 강력한 순서 보장과 리플레이 기능이 필요한 데이터 중심 작업.
- **RabbitMQ**를 **Lightweight Task Queue**로 선정한다.
  - 순수 비동기 작업(Async jobs) 및 저지연 메시지 전달용.
  - AMQP 표준을 기반으로 한 복잡한 라우팅 규칙(Exchange)이 필요한 경우.
- **Kafka KRaft Mode**를 채택하여 Zookeeper 의존성을 제거하고 클러스터 관리를 단순화한다.

## Explicit Non-goals

- Redis Pub/Sub을 대체하지 않음 (Zustand/In-memory 상태 용도 제외).
- Cloud Native Messaging (SQS/SNS) 연동 전략은 이 ADR 범위 밖.

## Consequences

- **Positive**:
  - 용도별 최적의 도구 사용으로 시스템 성능 및 유연성 확보.
  - Kafka KRaft 모드 도입으로 인프라 리소스 절약 및 배포 단순화.
- **Trade-offs**:
  - 두 가지 솔루션을 모두 운영해야 하는 비용(이미지 크기, 메모리 사용량).
  - 개발자가 어떤 도구를 사용할지에 대한 가이드라인 숙지 필요.

## Alternatives

### [Only Apache Kafka]

- Good: 단일 스택 운영 편의성.
- Bad: 단순한 태스크 큐잉을 위해 오프셋 관리 및 파티션 할당 로직이 과해질 수 있음.

### [Only RabbitMQ]

- Good: 뛰어난 라우팅의 유연성과 단순성.
- Bad: 로그 스트리밍과 같은 대용량 데이터의 수평 확장성 및 리플레이 기능 부족.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-05-messaging.md]`
- **ARD**: `[../02.ard/0005-messaging-architecture.md]`
- **Spec**: `[../04.specs/05-messaging/spec.md]`
- **Plan**: `[../05.plans/2026-03-26-05-messaging-standardization.md]`
