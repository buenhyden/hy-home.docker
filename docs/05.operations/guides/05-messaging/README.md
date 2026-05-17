# Messaging Operations Policy (05.operations/05-messaging)

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

- 단계별 장애 복구 실행 절차 (-> `05.operations/05-messaging`)
- 개발자 사용 튜토리얼 (-> `05.operations/05-messaging`)

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
2. 정책 변경 시 대응 Procedure/GUIDE 링크를 함께 갱신한다.
3. 카탈로그 항목과 정책 통제를 매핑해 변경 근거를 남긴다.
4. 문서 변경 후 `scripts/validation/check-doc-traceability.sh`를 실행한다.

## Usage Instructions

이 경로는 "무엇을 허용/금지하는가"를 정의하는 정책 계층이다. 구체 실행 절차는 `05.operations`를 참조한다.

## Verification and Monitoring

- 정책 준수 검증:
  - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- 메시징 운영 지표:
  - Kafka ISR/lag
  - RabbitMQ queue depth/unacked messages

## Incident and Recovery Links

- **Procedures**: [../../05.operations/05-messaging/README.md](./README.md)
- **Usages**: [../../05.operations/05-messaging/README.md](./README.md)

## SSoT References

- **PRD**: [2026-03-28-05-messaging-optimization-hardening.md](../../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [0020-messaging-optimization-hardening-architecture.md](../../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [0020-messaging-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [05-messaging Spec](../../../03.specs/05-messaging/spec.md)
- **Plan**: [2026-03-28-05-messaging-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [2026-03-28-05-messaging-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Procedure**: [optimization-hardening.md](../../policies/05-messaging/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../../policies/12-infra-service-optimization-catalog.md)

## AI Agent Guidance

1. 라우팅/접근제어 변경 시 `optimization-hardening.md` 정책을 우선 기준으로 적용한다.
2. 정책 문서에서 정한 Required 통제를 compose 변경에서 누락하면 안 된다.

---

## Related Documents

- [docs/05.operations/README.md](../../README.md)
- [docs/05.operations/README.md](../../README.md)
- [docs/05.operations/README.md](../../README.md)

## Usage

> Migrated from `docs/05.operations/05-messaging/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Messaging Usages (05.operations/05-messaging)

> Developer/operator guides for Kafka, RabbitMQ, stream processing, and optimization hardening.

#### Overview

이 디렉터리는 `05-messaging` 계층의 사용/운영 가이드를 제공한다. Kafka, RabbitMQ, ksql 스트리밍, 그리고 optimization-hardening 적용 절차를 문서화한다.

#### Audience

이 README의 주요 독자:

- Developers
- Messaging Operators
- DevOps Engineers
- AI Agents

#### Scope

##### In Scope

- Kafka 사용/운영 가이드
- RabbitMQ 사용/운영 가이드
- ksql 스트리밍 가이드
- 메시징 최적화/하드닝 적용 가이드

##### Out of Scope

- 운영 통제 정책 정의 (-> `05.operations/05-messaging`)
- 즉시 실행 장애 복구 절차 (-> `05.operations/05-messaging`)

#### Structure

```text
05-messaging/
├── kafka.md                    # Kafka cluster guide
├── rabbitmq.md                 # RabbitMQ usage guide
├── 03.ksql-streaming.md        # ksql streaming guide
├── optimization-hardening.md   # Messaging optimization/hardening guide
└── README.md                   # This file
```

#### How to Work in This Area

1. 새 가이드는 `docs/99.templates/operation.template.md`를 기반으로 작성한다.
2. 절차성 문서에는 반드시 Prerequisites와 Step-by-step Instructions를 포함한다.
3. 관련 Spec/Operation/Procedure 링크를 문서 하단에 유지한다.
4. 가이드 파일을 추가/변경하면 이 README의 Structure와 SSoT 링크를 즉시 갱신한다.

#### Documentation Standards

- 가이드는 정책 문서가 아닌 실행 가능한 설명 문서여야 한다.
- 상대 경로 링크만 사용한다.
- 한국어 `Overview (KR)` 요약을 포함한다.

#### SSoT References

- **PRD**: [2026-03-28-05-messaging-optimization-hardening.md](../../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [0020-messaging-optimization-hardening-architecture.md](../../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [0020-messaging-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [05-messaging Spec](../../../03.specs/05-messaging/spec.md)
- **Plan**: [2026-03-28-05-messaging-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [2026-03-28-05-messaging-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Operation**: [optimization-hardening.md](../../policies/05-messaging/optimization-hardening.md)
- **Procedure**: [optimization-hardening.md](../../policies/05-messaging/optimization-hardening.md)

#### AI Agent Guidance

1. 메시징 가이드 수정 시 optimization-hardening 문서와 상호 링크를 유지한다.
2. 관리 경로 정책(SSO/middleware) 관련 설명은 `05.operations` 기준과 충돌하지 않아야 한다.

---

#### Related Documents

- [docs/05.operations/README.md](../../README.md)
- [docs/05.operations/README.md](../../README.md)
- [docs/05.operations/README.md](../../README.md)

## Procedure

> Migrated from `docs/05.operations/05-messaging/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Messaging Procedures (05.operations/05-messaging)

> Executable procedures for messaging incident response, recovery, and optimization baseline restoration.

#### Overview

이 디렉터리는 `05-messaging` 계층의 즉시 실행 가능한 운영 절차를 제공한다. Kafka/RabbitMQ 장애 복구와 optimization-hardening 회귀 복구 절차를 포함한다.

#### Audience

이 README의 주요 독자:

- SRE / On-call Engineers
- DevOps Engineers
- Messaging Operators
- AI Agents

#### Scope

##### In Scope

- Kafka 장애 대응/복구 절차
- RabbitMQ 장애 대응/복구 절차
- 메시징 optimization-hardening 회귀 복구 절차

##### Out of Scope

- 운영 통제 정의 (-> `05.operations/05-messaging`)
- 교육용/개념 중심 가이드 (-> `05.operations/05-messaging`)

#### Structure

```text
05-messaging/
├── kafka.md                    # Kafka recovery and maintenance
├── rabbitmq.md                 # RabbitMQ recovery and maintenance
├── optimization-hardening.md   # Messaging hardening baseline recovery
└── README.md                   # This file
```

#### How to Work in This Area

1. 런북은 즉시 실행 가능한 절차와 검증 단계를 우선으로 작성한다.
2. `docs/99.templates/operation.template.md` 형식을 준용한다.
3. 위험 조치 전 승인 조건과 복구 증적 수집 방법을 명시한다.
4. 문서 추가/변경 시 README 구조와 SSoT 링크를 함께 갱신한다.

#### Usage Instructions

장애 유형에 맞는 런북을 선택하고, Checklist -> Procedure -> Verification 순서로 수행한다.

#### Verification and Monitoring

- 런북 수행 후 `Verification Steps`를 반드시 완료한다.
- 필요 시 다음 검증을 병행한다.
  - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
  - `bash scripts/validation/check-doc-traceability.sh`

#### Incident and Recovery Links

- **Operations Policy**: [../../05.operations/05-messaging/README.md](./README.md)
- **Usages**: [../../05.operations/05-messaging/README.md](./README.md)

#### SSoT References

- **PRD**: [2026-03-28-05-messaging-optimization-hardening.md](../../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [0020-messaging-optimization-hardening-architecture.md](../../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [0020-messaging-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [05-messaging Spec](../../../03.specs/05-messaging/spec.md)
- **Plan**: [2026-03-28-05-messaging-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [2026-03-28-05-messaging-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Operation**: [optimization-hardening.md](../../policies/05-messaging/optimization-hardening.md)

#### AI Agent Guidance

1. 고위험 조치(큐 purge, 강제 재배치, 접근제어 완화) 전 사람 승인 필요.
2. 수행 전후 상태 증적(health, logs, config diff)을 남기고 incident 기록으로 연결한다.

---

#### Related Documents

- [docs/05.operations/README.md](../../README.md)
- [docs/05.operations/README.md](../../README.md)
- [docs/05.operations/incidents/README.md](../../incidents/README.md)
