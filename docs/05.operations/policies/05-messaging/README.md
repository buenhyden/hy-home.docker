<!-- README Target: docs/05.operations/policies/05-messaging/README.md -->

# Operations Policies - 05 Messaging

> 운영 통제, 보안/가용성 기준, 예외 승인 기준을 관리한다.

## Overview

`policies/05-messaging`는 `docs/05.operations`의 policy 문서를 관리합니다. 필수/허용/금지 상태, 예외 승인, 검증 기준, 검토 주기를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 운영 controls, allowed/disallowed 상태, exception, review cadence
- 현재 경로에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/05-messaging/
├── kafka.md
├── optimization-hardening.md
├── rabbitmq.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [kafka.md](./kafka.md) | Kafka policy 문서 |
| [optimization-hardening.md](./optimization-hardening.md) | Optimization Hardening policy 문서 |
| [rabbitmq.md](./rabbitmq.md) | Rabbitmq policy 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Policies index](../README.md)
- [Operations Guides - 05-messaging](../../guides/05-messaging/README.md)
- [Operations Runbooks - 05-messaging](../../runbooks/05-messaging/README.md)
- [Incident records](../../incidents/README.md)
