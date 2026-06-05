<!-- README Target: docs/05.operations/policies/README.md -->

# Operations Policies

> 운영 통제, 보안/가용성 기준, 예외 승인 기준을 관리한다.

## Overview

`policies`는 `docs/05.operations`의 운영 정책 문서를 관리합니다.
필수/허용/금지 상태, 예외 승인 기준, 검증 기준, 검토 주기를 제공합니다.
guide, policy, runbook의 목적을 섞지 않고, 운영자가 적용해야 할 통제 기준을
빠르게 확인하도록 돕습니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 운영 controls, allowed/disallowed 상태, exception, review cadence
- 이 bucket에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation
- 사람이 읽는 한국어 통제 설명과 원형을 유지해야 하는 control name,
  evidence ID, 명령, 경로, 서비스명, 환경 변수, secret ID

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/
├── 00-workspace/
├── 01-gateway/
├── 02-auth/
├── 03-security/
├── 04-data/
├── 05-messaging/
├── 06-observability/
├── 07-workflow/
├── 08-ai/
├── 09-tooling/
├── 10-communication/
├── 11-laboratory/
├── 12-infra-net/
├── 90-knowledge/
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.
3. policy leaf 문서는 `docs/99.templates/policy.template.md`의 단일 `## Policy Scope` 섹션에 시스템, 구성 파일, agent, environment 범위를 함께 기록합니다.
4. 본문은 한국어로 쓰되 control name, evidence ID, 명령, 경로, 서비스명,
   환경 변수, Docker profile, secret ID는 원형을 유지합니다.

## Contents

| Path | Purpose |
| --- | --- |
| [00-workspace/](./00-workspace/README.md) | Workspace-level policy 문서 |
| [01-gateway/](./01-gateway/README.md) | Gateway Traefik/Nginx hardening and runtime-boundary policies |
| [02-auth/](./02-auth/README.md) | 02 Auth policy 문서 |
| [03-security/](./03-security/README.md) | 03 Security policy 문서 |
| [04-data/](./04-data/README.md) | 04 Data policy 문서 |
| [05-messaging/](./05-messaging/README.md) | 05 Messaging policy 문서 |
| [06-observability/](./06-observability/README.md) | 06 Observability policy 문서 |
| [07-workflow/](./07-workflow/README.md) | 07 Workflow policy 문서 |
| [08-ai/](./08-ai/README.md) | 08 Ai policy 문서 |
| [09-tooling/](./09-tooling/README.md) | 09 Tooling policy 문서 |
| [10-communication/](./10-communication/README.md) | 10 Communication policy 문서 |
| [11-laboratory/](./11-laboratory/README.md) | 11 Laboratory policy 문서 |
| [12-infra-net/](./12-infra-net/README.md) | infra_net IP 관리 policy 문서 |
| [90-knowledge/](./90-knowledge/README.md) | Knowledge maintenance policy 문서 |

## Related Documents

- [Operations index](../README.md)
- [Operations Guides](../guides/README.md)
- [Operations Runbooks](../runbooks/README.md)
- [Incident records](../incidents/README.md)
