# Messaging Guides (07.guides/05-messaging)

> Developer guides for event streaming, message brokering, and streaming analytics.

## Overview

이 디렉터리는 `hy-home.docker`의 메시징 인프라(05-messaging)를 사용하는 개발자와 운영자를 위한 기술 가이드를 포함한다. Kafka, RabbitMQ 등의 메시지 브로커 연동, 스키마 관리 및 실시간 데이터 처리 절차를 다룬다.

## Audience

이 README의 주요 독자:

- **Developers**: 앱 연동 및 메시지 생산/소비 절차 파악.
- **Operators**: 시스템 구성 요소 및 관리 도구 활용법 숙지.
- **AI Agents**: 자동화된 시스템 점검 및 설정 가이드 참조.

## Scope

### In Scope

- **Kafka Strategy**: KRaft 기반 클러스터 사용법 및 토픽 관리.
- **RabbitMQ Patterns**: AMQP 큐 모델 및 워크로드 분산 가이드.
- **Streaming Logic**: ksqlDB 등을 활용한 실시간 분석 절차.

### Out of Scope

- 하부 인프라(Docker/VM) 프로비저닝 (01-gateway 계층 담당).
- 애플리케이션 프레임워크별 라이브러리 상세 사용법.

## Structure

```text
05-messaging/
├── kafka.md           # Kafka Cluster Setup & Usage
├── rabbitmq.md        # RabbitMQ Usage Guide
├── 03.ksql-streaming.md # Streaming Analytics Guide
└── README.md          # This file
```

## How to Work in This Area

1. **New Guide**: 새 가이드는 `docs/99.templates/guide.template.md`를 사용하여 작성한다.
2. **Standardization**: 모든 절차는 명확한 `Prerequisites`와 `Step-by-step Instructions`를 포함해야 한다.
3. **Traceability**: 작성 시 `Spec` 및 `Operation` 문서와 링크를 유지한다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 기존 SSoT (Single Source of Truth, 단일 진실 원천) 문서를 중복 생성하지 않는다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.

## SSoT References

- **PRD**: [05-messaging](../../01.prd/2026-03-26-05-messaging.md)
- **ARD**: [Messaging Architecture](../../02.ard/0005-messaging-architecture.md)
- **Spec**: [05-messaging Spec](../../04.specs/05-messaging/spec.md)
- **Plan**: [Messaging Plan](../../01.prd/2026-03-26-05-messaging.md)

## AI Agent Guidance

1. 이 영역의 문서를 수정할 때 기존의 `Related Documents` 링크 무결성을 유지할 것.
2. 새 가이드 추가 시 본 `README.md`의 `Structure` 섹션을 즉시 업데이트할 것.
