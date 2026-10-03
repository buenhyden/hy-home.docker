---
title: "메시징 계층 (05-messaging)"
version: "1.1.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2025-11-12"
---

# 05 메시징

## Overview

이 tier는 현재 [`kafka`](kafka/README.md) 패키지 하나를 포함합니다. OPTIONAL
Kafka-family 이벤트 스트리밍 surface이며 두 번째 broker family는 없습니다.

## Audience

이 패키지 맵은 messaging tier의 operator와 maintainer를 위한 것입니다.

## Scope

현재 Kafka 패키지와 그 루트 Compose selector를 다룹니다.

## Structure

이 tier의 leaf 패키지는 [`kafka`](kafka/README.md) 하나입니다.

## Tech Stack

정상 Kafka와 주변 서비스의 이미지 선언은 [`kafka/`](kafka/README.md)가 소유합니다.

## Configuration

루트 include는 정상 선택형 구성만 포함합니다. 다중 브로커 LAB의 독립 환경·상태는 [`labs/kafka-cluster.yml`](../../labs/kafka-cluster.yml)이 소유합니다.

## Validation

정상 선택자와 LAB 진입점을 각각 Compose 렌더로 확인하고, 실제 기동 결과는 별도로 기록합니다.

## How to Work in This Area

정확한 루트 selector는 `messaging`, `messaging-broker`,
`messaging-schema`, `messaging-connect`, `messaging-rest`,
`messaging-admin`입니다. 각 selector가 선택하는 서비스는 패키지 맵을
참고하십시오. 활성화 전에는 named producer/consumer, retention/capacity
계획, plaintext-listener 위험 수용, 완전한 복구 계획이 필요합니다. 한
별도 `labs/kafka-cluster.yml`의 세 broker도 한 호스트에서는 host availability가 아닙니다.

## Related Documents

[문서 진입점](../../docs/README.md)을 사용해 Stage 05 Messaging subject
`docs/05.operations/guides/0036-kafka.md`와
`docs/05.operations/guides/0037-messaging-optimization-hardening.md`을
찾으십시오.
