# Messaging Guides (07.guides/05-messaging)

> Developer/operator guides for Kafka, RabbitMQ, stream processing, and optimization hardening.

## Overview

이 디렉터리는 `05-messaging` 계층의 사용/운영 가이드를 제공한다. Kafka, RabbitMQ, ksql 스트리밍, 그리고 optimization-hardening 적용 절차를 문서화한다.

## Audience

이 README의 주요 독자:

- Developers
- Messaging Operators
- DevOps Engineers
- AI Agents

## Scope

### In Scope

- Kafka 사용/운영 가이드
- RabbitMQ 사용/운영 가이드
- ksql 스트리밍 가이드
- 메시징 최적화/하드닝 적용 가이드

### Out of Scope

- 운영 통제 정책 정의 (-> `08.operations/05-messaging`)
- 즉시 실행 장애 복구 절차 (-> `09.runbooks/05-messaging`)

## Structure

```text
05-messaging/
├── kafka.md                    # Kafka cluster guide
├── rabbitmq.md                 # RabbitMQ usage guide
├── 03.ksql-streaming.md        # ksql streaming guide
├── optimization-hardening.md   # Messaging optimization/hardening guide
└── README.md                   # This file
```

## How to Work in This Area

1. 새 가이드는 `docs/99.templates/guide.template.md`를 기반으로 작성한다.
2. 절차성 문서에는 반드시 Prerequisites와 Step-by-step Instructions를 포함한다.
3. 관련 Spec/Operation/Runbook 링크를 문서 하단에 유지한다.
4. 가이드 파일을 추가/변경하면 이 README의 Structure와 SSoT 링크를 즉시 갱신한다.

## Documentation Standards

- 가이드는 정책 문서가 아닌 실행 가능한 설명 문서여야 한다.
- 상대 경로 링크만 사용한다.
- 한국어 `Overview (KR)` 요약을 포함한다.

## SSoT References

- **PRD**: [2026-03-28-05-messaging-optimization-hardening.md](../../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [0020-messaging-optimization-hardening-architecture.md](../../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [0020-messaging-hardening-and-ha-expansion-strategy.md](../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [05-messaging Spec](../../04.specs/05-messaging/spec.md)
- **Plan**: [2026-03-28-05-messaging-optimization-hardening-plan.md](../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [2026-03-28-05-messaging-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Operation**: [optimization-hardening.md](../../08.operations/05-messaging/optimization-hardening.md)
- **Runbook**: [optimization-hardening.md](../../09.runbooks/05-messaging/optimization-hardening.md)

## AI Agent Guidance

1. 메시징 가이드 수정 시 optimization-hardening 문서와 상호 링크를 유지한다.
2. 관리 경로 정책(SSO/middleware) 관련 설명은 `08.operations` 기준과 충돌하지 않아야 한다.
