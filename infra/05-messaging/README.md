---
title: "Messaging Tier (05-messaging)"
version: "1.1.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# 05 Messaging

## Overview

이 tier는 현재 [`kafka`](kafka/README.md) 패키지 하나를 포함합니다. OPTIONAL
Kafka-family 이벤트 스트리밍 surface이며 두 번째 broker family는 없습니다.

## Audience

이 패키지 맵은 messaging tier의 operator와 maintainer를 위한 것입니다.

## Scope

현재 Kafka 패키지와 그 루트 Compose selector를 다룹니다.

## Structure

이 tier의 leaf 패키지는 [`kafka`](kafka/README.md) 하나입니다.

## How to Work in This Area

정확한 루트 selector는 `messaging`, `messaging-broker`, `messaging-cluster`,
`messaging-schema`, `messaging-connect`, `messaging-rest`,
`messaging-admin`입니다. 각 selector가 선택하는 서비스는 패키지 맵을
참고하십시오. 활성화 전에는 named producer/consumer, retention/capacity
계획, plaintext-listener 위험 수용, 완전한 복구 계획이 필요합니다. 한
호스트의 broker 3개는 host availability가 아닙니다.

## Related Documents

[문서 진입점](../../docs/README.md)을 사용해 Stage 05 Messaging subject
`docs/05.operations/guides/0036-kafka.md`와
`docs/05.operations/guides/0037-messaging-optimization-hardening.md`을
찾으십시오.
