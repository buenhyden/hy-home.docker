# Messaging Runbooks (09.runbooks/05-messaging)

> Executable procedures for messaging incident response, recovery, and optimization baseline restoration.

## Overview

이 디렉터리는 `05-messaging` 계층의 즉시 실행 가능한 운영 절차를 제공한다. Kafka/RabbitMQ 장애 복구와 optimization-hardening 회귀 복구 절차를 포함한다.

## Audience

이 README의 주요 독자:

- SRE / On-call Engineers
- DevOps Engineers
- Messaging Operators
- AI Agents

## Scope

### In Scope

- Kafka 장애 대응/복구 절차
- RabbitMQ 장애 대응/복구 절차
- 메시징 optimization-hardening 회귀 복구 절차

### Out of Scope

- 운영 통제 정의 (-> `08.operations/05-messaging`)
- 교육용/개념 중심 가이드 (-> `07.guides/05-messaging`)

## Structure

```text
05-messaging/
├── kafka.md                    # Kafka recovery and maintenance
├── rabbitmq.md                 # RabbitMQ recovery and maintenance
├── optimization-hardening.md   # Messaging hardening baseline recovery
└── README.md                   # This file
```

## How to Work in This Area

1. 런북은 즉시 실행 가능한 절차와 검증 단계를 우선으로 작성한다.
2. `docs/99.templates/runbook.template.md` 형식을 준용한다.
3. 위험 조치 전 승인 조건과 복구 증적 수집 방법을 명시한다.
4. 문서 추가/변경 시 README 구조와 SSoT 링크를 함께 갱신한다.

## Usage Instructions

장애 유형에 맞는 런북을 선택하고, Checklist -> Procedure -> Verification 순서로 수행한다.

## Verification and Monitoring

- 런북 수행 후 `Verification Steps`를 반드시 완료한다.
- 필요 시 다음 검증을 병행한다.
  - `bash scripts/check-messaging-hardening.sh`
  - `bash scripts/check-doc-traceability.sh`

## Incident and Recovery Links

- **Operations Policy**: [../../08.operations/05-messaging/README.md](../../08.operations/05-messaging/README.md)
- **Guides**: [../../07.guides/05-messaging/README.md](../../07.guides/05-messaging/README.md)

## SSoT References

- **PRD**: [2026-03-28-05-messaging-optimization-hardening.md](../../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [0020-messaging-optimization-hardening-architecture.md](../../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [0020-messaging-hardening-and-ha-expansion-strategy.md](../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [05-messaging Spec](../../04.specs/05-messaging/spec.md)
- **Plan**: [2026-03-28-05-messaging-optimization-hardening-plan.md](../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [2026-03-28-05-messaging-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Operation**: [optimization-hardening.md](../../08.operations/05-messaging/optimization-hardening.md)

## AI Agent Guidance

1. 고위험 조치(큐 purge, 강제 재배치, 접근제어 완화) 전 사람 승인 필요.
2. 수행 전후 상태 증적(health, logs, config diff)을 남기고 incident 기록으로 연결한다.
