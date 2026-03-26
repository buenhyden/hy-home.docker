# Kafka Cluster Operations Policy (05-messaging)

> Governance, Data Retention, and Reliability Standards for Kafka.

---

## Overview (KR)

이 문서는 Kafka 클러스터(05-messaging)의 운영 정책을 정의한다. 메시지 보관(Retention), 복제(Replication), 그리고 스키마 거버넌스에 대한 필수 통제 기준을 포함한다.

## Policy Scope

이 정책은 Kafka 브로커, 스키마 레지스트리, 그리고 클러스터 내의 모든 토픽 설정을 제어한다.

## Applies To

- **Systems**: Kafka Broker Cluster (3-node), Schema Registry
- **Agents**: AI Infrastructure Agent, CI/CD Deployer
- **Environments**: Production (Default), Development

## Controls

### 1. Topic## Replication Policy

- **Min ISR**: 2 (가용성 확보).
토픽은 최소 `replication.factor=3` 및 `min.insync.replicas=2`를 유지해야 한다.
- **Required**: `infra-events`, `application-logs` 등 핵심 토픽은 삭제(`delete`) 정책을 비활성화하거나 유예 기간을 두어야 한다.

### 2. Data## Retention Standards

- **Internal Events**: 7일 보관 (Compact 정책 병행).
ms`는 7일(604,800,000ms)로 설정한다.
- **Allowed**: 중요 회계/보안 이벤트의 경우 최대 30일까지 확장 가능하나 인프라 용량 검토가 선행되어야 한다.
- **Disallowed**: 스토리지 고갈 방지를 위해 `retention.bytes` 제한 없는 토픽 생성을 금지한다.

### 3.## Schema Governance

- **Compatibility**: `BACKWARD`를 기본값으로 설정.
`Schema Registry`를 통해 메시지 형식을 유효화해야 한다.
- **Allowed**: `BACKWARD` 호환성 모드를 기본값으로 사용한다.
- **Disallowed**: 시스템 중단을 초래할 수 있는 호환성 없는 스키마의 강제 업데이트(`NONE` 모드)를 금지한다.

## Exceptions

- 단기 성능 테스트용 토픽의 경우 `replication.factor=1`을 부분적으로 허용하나, 작업 완료 후 즉각 삭제해야 한다. (DevOps 팀 승인 필요)

## Verification

- **Compliance Check**: Kafbat UI 또는 CLI를 통해 토픽 설정이 정책과 일치하는지 주간 단위로 감사한다.
- **Cluster Audit**: `UnderReplicatedPartitions` 지표를 상시 감시하여 가용성 정책 위반을 감지한다.

## Review Cadence

- Quarterly (분기별) 데이터 용량 및 정책 실효성 검토.

## AI Agent Policy Section

- **Automated Topic Creation**: `kafka-init` 서비스를 통해서만 자동 생성이 허용되며, 생성 시 필수 라벨(`hy-home.tier`)이 포함되어야 한다.
- **Health Guardrails**: 복제 오류 발생 시 AI Agent는 신규 생산자 연결을 일시 중단하거나 경고를 전송해야 한다.

## Related Documents

- **ARD**: `[../../02.ard/0005-messaging-architecture.md]`
- **Runbook**: `[../../09.runbooks/05-messaging/kafka.md]`
- **Guide**: `[../../07.guides/05-messaging/kafka.md]`
