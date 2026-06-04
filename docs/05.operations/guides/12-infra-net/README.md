<!-- README Target: docs/05.operations/guides/12-infra-net/README.md -->

# Operations Guides - 12 Infra Net

> infra_net 표준화와 고정 IP 운영 사용 맥락을 관리한다.

## Overview

`guides/12-infra-net`는 `docs/05.operations`의 infra_net guide 문서를 관리합니다. 네트워크 표준화 작업자가 authoritative mapping과 관련 runbook handoff를 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- infra_net 사용 맥락, 설정 방법, 일반 점검
- 현재 경로에 속한 guide 문서 인덱스
- 관련 policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 서비스별 compose 구현 세부 명세
- 운영 통제 기준과 반복 실행 복구 절차
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/12-infra-net/
├── standardize-infra-net.md
└── README.md
```

## How to Work in This Area

1. infra_net guide를 추가, 이동, 삭제하면 이 README와 `guides/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [standardize-infra-net.md](./standardize-infra-net.md) | infra_net 네트워크 표준화 guide 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 12-infra-net](../../policies/12-infra-net/README.md)
- [Operations Runbooks - 12-infra-net](../../runbooks/12-infra-net/README.md)
- [Incident records](../../incidents/README.md)
