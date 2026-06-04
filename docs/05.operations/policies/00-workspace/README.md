<!-- README Target: docs/05.operations/policies/00-workspace/README.md -->

# Operations Policies - 00 Workspace

> 서비스 티어 하나에만 속하지 않는 workspace-level 운영 통제와 예외 기준을 관리한다.

## Overview

`policies/00-workspace`는 `docs/05.operations`의 workspace-level policy 문서를 관리합니다. harness 운영, 공통 최적화 예외, 인프라 서비스 최적화 catalog처럼 저장소 전체 운영 기준에 가까운 policy를 한 곳에 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- workspace-level controls, allowed/disallowed 상태, exception, review cadence
- 현재 경로에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 개별 서비스 티어 policy
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/00-workspace/
├── common-optimizations-template-exceptions.md
├── harness-agent-first-engineering.md
├── infra-service-optimization-catalog.md
└── README.md
```

## How to Work in This Area

1. workspace-level policy를 추가, 이동, 삭제하면 이 README와 `policies/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [common-optimizations-template-exceptions.md](./common-optimizations-template-exceptions.md) | Common optimizations template exceptions policy 문서 |
| [harness-agent-first-engineering.md](./harness-agent-first-engineering.md) | Harness / Agent-first Engineering policy 문서 |
| [infra-service-optimization-catalog.md](./infra-service-optimization-catalog.md) | Infra service optimization catalog policy 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Policies index](../README.md)
- [Operations Guides - 00-workspace](../../guides/00-workspace/README.md)
- [Operations Runbooks - 00-workspace](../../runbooks/00-workspace/README.md)
- [Incident records](../../incidents/README.md)
