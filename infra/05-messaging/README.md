---
title: "메시징 계층 (05-messaging)"
version: "1.1.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

# 05 메시징

## Purpose

### Service Role

이 tier는 현재 [`kafka`](kafka/README.md) 패키지 하나를 포함합니다. OPTIONAL
Kafka-family 이벤트 스트리밍 surface이며 두 번째 broker family는 없습니다.

#### Audience

이 패키지 맵은 messaging tier의 operator와 maintainer를 위한 것입니다.

현재 Kafka 패키지와 그 루트 Compose selector를 다룹니다.

#### Structure

이 tier의 leaf 패키지는 [`kafka`](kafka/README.md) 하나입니다.

### Supported Environment

정상 Kafka와 주변 서비스의 이미지 선언은 [`kafka/`](kafka/README.md)가 소유합니다.

## Interfaces

### Inputs and Outputs

루트 include는 정상 선택형 구성만 포함합니다.

### Security Boundary

없음: 이 디렉터리는 Compose 서비스나 secret 참조를 직접 선언하지 않으며, 하위 `kafka/`가 각자 선언한다.

## Development

### Local Workflow

정확한 루트 selector는 `messaging`, `messaging-broker`,
`messaging-admin`입니다. 각 selector가 선택하는 서비스는 패키지 맵을
참고하십시오. 활성화 전에는 named producer/consumer, retention/capacity
계획, plaintext-listener 위험 수용, 완전한 복구 계획이 필요합니다.

### Checks

정상 선택자를 Compose 렌더로 확인하고, 실제 기동 결과는 별도로 기록합니다.

## Operations

### Runbook Links

#### Related Documents

[문서 진입점](../../docs/README.md)을 사용해 Stage 05 Messaging subject
`docs/05.operations/guides/06-messaging-and-cdc/0036-kafka.md`와
`docs/05.operations/guides/06-messaging-and-cdc/0037-messaging-optimization-hardening.md`을
찾으십시오.

### Observability and Recovery

없음: 이 디렉터리는 자체 헬스체크나 관측 대상을 선언하지 않으며, 하위 `kafka/`가 각자 선언한다.
