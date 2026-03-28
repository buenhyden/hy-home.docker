# Messaging Operations Policy (08.operations/05-messaging)

> Governance, reliability standards, and optimization/hardening controls for the messaging tier.

## Overview

이 디렉터리는 `05-messaging` 계층의 운영 정책 문서를 관리한다. Kafka/RabbitMQ 운영 기준, 보안/가용성 통제, 카탈로그 기반 확장 승인 조건을 정의한다.

## Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Architects
- AI Agents

## Scope

### In Scope

- Kafka 운영 정책
- RabbitMQ 운영 정책
- 메시징 optimization/hardening 운영 정책
- 카탈로그 연계 운영 통제 기준

### Out of Scope

- 단계별 장애 복구 실행 절차 (-> `09.runbooks/05-messaging`)
- 개발자 사용 튜토리얼 (-> `07.guides/05-messaging`)

## Structure

```text
05-messaging/
├── kafka.md                    # Kafka operations policy
├── rabbitmq.md                 # RabbitMQ operations policy
├── optimization-hardening.md   # Messaging optimization/hardening policy
└── README.md                   # This file
```

## How to Work in This Area

1. 정책 문서는 `docs/99.templates/operation.template.md`를 기준으로 작성한다.
2. 정책 변경 시 대응 Runbook/GUIDE 링크를 함께 갱신한다.
3. 카탈로그 항목과 정책 통제를 매핑해 변경 근거를 남긴다.
4. 문서 변경 후 `scripts/check-doc-traceability.sh`를 실행한다.

## Usage Instructions

이 경로는 "무엇을 허용/금지하는가"를 정의하는 정책 계층이다. 구체 실행 절차는 `09.runbooks`를 참조한다.

## Verification and Monitoring

- 정책 준수 검증:
  - `bash scripts/check-messaging-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- 메시징 운영 지표:
  - Kafka ISR/lag
  - RabbitMQ queue depth/unacked messages

## Incident and Recovery Links

- **Runbooks**: [../../09.runbooks/05-messaging/README.md](../../09.runbooks/05-messaging/README.md)
- **Guides**: [../../07.guides/05-messaging/README.md](../../07.guides/05-messaging/README.md)

## SSoT References

- **PRD**: [2026-03-28-05-messaging-optimization-hardening.md](../../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [0020-messaging-optimization-hardening-architecture.md](../../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [0020-messaging-hardening-and-ha-expansion-strategy.md](../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [05-messaging Spec](../../04.specs/05-messaging/spec.md)
- **Plan**: [2026-03-28-05-messaging-optimization-hardening-plan.md](../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [2026-03-28-05-messaging-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Runbook**: [optimization-hardening.md](../../09.runbooks/05-messaging/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## AI Agent Guidance

1. 라우팅/접근제어 변경 시 `optimization-hardening.md` 정책을 우선 기준으로 적용한다.
2. 정책 문서에서 정한 Required 통제를 compose 변경에서 누락하면 안 된다.
