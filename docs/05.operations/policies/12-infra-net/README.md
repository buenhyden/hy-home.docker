<!-- README Target: docs/05.operations/policies/12-infra-net/README.md -->

# Operations Policies - 12 Infra Net

> infra_net 표준화와 고정 IP 운영 통제를 관리한다.

## Overview

`policies/12-infra-net`는 `docs/05.operations`의 infra_net policy 문서를 관리합니다. 고정 IP 관리, 예외 기준, 검증 기준, review cadence를 guide/runbook과 분리해 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- infra_net controls, allowed/disallowed 상태, exception, review cadence
- 현재 경로에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 개별 서비스 티어 policy
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/12-infra-net/
├── standardize-infra-net.md
└── README.md
```

## How to Work in This Area

1. infra_net policy를 추가, 이동, 삭제하면 이 README와 `policies/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [standardize-infra-net.md](./standardize-infra-net.md) | infra_net IP management policy 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Policies index](../README.md)
- [Operations Guides - 12-infra-net](../../guides/12-infra-net/README.md)
- [Operations Runbooks - 12-infra-net](../../runbooks/12-infra-net/README.md)
- [Incident records](../../incidents/README.md)
