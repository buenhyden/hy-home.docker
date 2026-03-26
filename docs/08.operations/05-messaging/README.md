# Messaging Operations Policy (08.operations/05-messaging)

> Governance, Reliability Standards, and Maintenance Policies for the Messaging Tier.

## Overview

이 디렉터리는 `hy-home.docker` 메시징 티어(05-messaging)의 운영 원칙과 데이터 관리 기준을 정의하는 정책 문서들을 포함한다. 시스템 가용성 보장과 데이터 정합성을 위한 표준 절차(Standard Procedures)를 규정한다.

## Audience

이 README의 주요 독자:

- **Operators**: 시스템 정책 수립 및 규준 준수 여부 점검.
- **Architects**: 메시징 아키텍처의 품질 속성(QA) 보장 확인.
- **AI Agents**: 운영 자동화 및 제어 정책 참조.

## Scope

### In Scope

- **Governance**: 데이터 보관(Retention), 스키마 거버넌스(Compatibility).
- **Standards**: 클러스터 가용성(Quorum) 유지 정책, 백프레셔(Backpressure) 통제.
- **Verification**: 정책 준수 여부 주기적 감사 절차.

### Out of Scope

- 개별 마이그레이션 실행 절차 (Runbook 영역).
- 개발 가이드 및 튜토리얼 (Guides 영역).

## Structure

```text
05-messaging/
├── kafka.md           # Kafka Operations Policy
├── rabbitmq.md        # RabbitMQ Operations Policy
└── README.md          # This file
```

## How to Work in This Area

1. **Policy Updates**: 기존 정책의 변경이 필요할 경우 `ARD`와의 일치 여부를 먼저 검토한다.
2. **Compliance**: 새로운 메시징 기술 도입 시 `operation.template.md`를 사용하여 운영 표준을 수립한다.
3. **Traceability**: 정책 문서는 가이드(`07.guides`) 및 런북(`09.runbooks`)과 상호 참조되어야 한다.

## Usage Instructions

이 경로의 문서는 운영자가 시스템 설정 시 준수해야 할 '규준(Policy)'을 제공한다. 구체적인 명령어 실행은 본 문서가 아닌 `09.runbooks`를 참조한다.

## Verification and Monitoring

- **Status Check**: [Grafana Dashboard]를 통해 실시간 정책 준수 상태(Lag, Replica 등)를 확인한다.
- **Audit**: `UnderReplicatedPartitions > 0` 발생 시 운영 정책 위반으로 간주하고 장애 대응 절차를 시작한다.

## Incident and Recovery Links

- **Runbooks**: [../../09.runbooks/05-messaging/README.md]
- **Guides**: [../../07.guides/05-messaging/README.md]

## AI Agent Guidance

1. 이 영역의 정책 수정 시 리드 타임 및 장애 영향도를 평가하는 워크플로를 우선 실행할 것.
2. 새 가용성 기준 설정 시 `spec.md`의 성능 목표치와 상충하지 않는지 확인할 것.
