# Messaging Runbooks (09.runbooks/05-messaging)

> Executable procedures for incident response, recovery, and recurring maintenance.

## Overview

이 디렉터리는 `hy-home.docker`의 메시징 인프라(05-messaging)에서 발생할 수 있는 주요 장애 상황의 복구 절차와 정기 점검 단계를 정의한 런북들을 포함한다. 운영자가 장애 상황에서 신속하고 정확하게 기술적 조치를 취할 수 있도록 단계별 안내를 제공한다.

## Audience

이 README의 주요 독자:

- **Site Reliability Engineers (SRE)**: 장애 대응 및 인프라 복구 실행.
- **DevOps Engineers**: 정기 유지보수 및 클러스터 튜닝.
- **AI Agents**: 자가 복구 워크플로 실행 및 장애 증거 수집.

## Scope

### In Scope

- **Recovery**: 브로커 쿼럼 복구, 스키마 오류 해결, 소비 지연(Lag) 해소 절차.
- **Maintenance**: 노드 순차 재시작, 파티션 재분산, 로그 세그먼트 정리.
- **Emergency**: 긴급 서비스 중단 및 롤백 절차.

### Out of Scope

- 운영 정책 및 규준 정의 (08.operations 계층 담당).
- 애플리케이션 코드 레벨의 버그 수정.

## Structure

```text
05-messaging/
├── kafka.md           # Kafka Recovery & Maintenance
├── rabbitmq.md        # RabbitMQ Recovery & Maintenance
└── README.md          # This file
```

## How to Work in This Area

1. **Immediate Execution**: 런북은 장황한 설명보다 즉시 실행 가능한 명령어 위주로 작성한다.
2. **Standardization**: 모든 런북은 [runbook.template.md](docs/99.templates/runbook.template.md) 형식을 준용한다.
3. **Evidence**: 복구 과정에서 수집해야 할 증거(Evidence)와 검증 기준을 명확히 명시한다.

## Usage Instructions

이 디렉터리의 문서는 사고 발생 시 가장 먼저 참조해야 하는 '행동 지침'이다. 각 런북은 특정 서비스나 상황에 대응하므로, 발생한 사건의 유형에 맞는 파일을 선택하여 `Procedure` 항목을 순서대로 수행한다.

## Verification and Monitoring

- **Signals**: 모니터링 시스템의 경고 발생 시 해당 런북의 `When to Use` 섹션을 확인한다.
- **Evidence**: 모든 작업 완료 후 `Verification Steps`를 수행하여 시스템 정상을 확정한다.

## Incident and Recovery Links

- **Operations Policy**: [../../08.operations/05-messaging/README.md]
- **Guides**: [../../07.guides/05-messaging/README.md]

## AI Agent Guidance

1. 장애 감지 시 적절한 런북을 식별하고 `Procedure`에 따른 환경 조사를 자율적으로 수행할 것.
2. 작업 수행 전후의 클러스터 상태를 캡처하여 `docs/10.incidents`에 보고서를 생성할 것.
3. 위험도가 높은 조치(예: Purge, Force 삭제) 전에는 반드시 사람의 명시적 승인을 요청할 것.
