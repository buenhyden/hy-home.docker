<!-- README Target: docs/05.operations/runbooks/12-infra-net/README.md -->

# Operations Runbooks - 12 Infra Net

> infra_net 표준화와 고정 IP 검증 절차를 관리한다.

## Overview

`runbooks/12-infra-net`는 `docs/05.operations`의 infra_net runbook 문서를 관리합니다. 고정 IP mapping 검증, 변경 전 점검, rollback/recovery, escalation 기준을 guide/policy와 분리해 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- infra_net validation, rollback, escalation, evidence capture
- 현재 경로에 속한 runbook 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 배경 설명 중심 가이드와 장기 운영 정책
- 개별 서비스 티어 runbook
- secret 값, credential, token, 인증서 원문

## Structure

```text
runbooks/12-infra-net/
├── standardize-infra-net.md
└── README.md
```

## How to Work in This Area

1. infra_net runbook을 추가, 이동, 삭제하면 이 README와 `runbooks/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [standardize-infra-net.md](./standardize-infra-net.md) | infra_net IP mapping validation and update runbook 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Runbooks index](../README.md)
- [Operations Guides - 12-infra-net](../../guides/12-infra-net/README.md)
- [Operations Policies - 12-infra-net](../../policies/12-infra-net/README.md)
- [Incident records](../../incidents/README.md)
