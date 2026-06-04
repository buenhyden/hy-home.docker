<!-- README Target: docs/05.operations/runbooks/README.md -->

<!-- Target: docs/05.operations/runbooks/README.md -->
# Operations Runbooks

> 복구, 검증, 반복 실행 절차를 명령과 evidence 중심으로 관리한다.

## Overview

`runbooks`는 `docs/05.operations`의 runbook 문서를 관리합니다. 트리거 조건, 순서 있는 절차, evidence, rollback/recovery, escalation을 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 장애 복구, 정기 점검, rollback, escalation, evidence capture
- 이 bucket에 속한 runbook 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 배경 설명 중심 가이드와 장기 운영 정책
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
runbooks/
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
├── 0012-standardize-infra-net.md
├── harness-agent-first-engineering-validation.md
├── llm-wiki-maintenance.md
├── release-management.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.
3. 명령 예시는 현재 구현에 맞는 실제 compose 경로, 이미지 태그, 고정 IP를 사용하고, 실행 가능한 절차에 복사 가능한 placeholder를 남기지 않습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [01-gateway/](./01-gateway/README.md) | 01 Gateway runbook 문서 |
| [02-auth/](./02-auth/README.md) | 02 Auth runbook 문서 |
| [03-security/](./03-security/README.md) | 03 Security runbook 문서 |
| [04-data/](./04-data/README.md) | 04 Data runbook 문서 |
| [05-messaging/](./05-messaging/README.md) | 05 Messaging runbook 문서 |
| [06-observability/](./06-observability/README.md) | 06 Observability runbook 문서 |
| [07-workflow/](./07-workflow/README.md) | 07 Workflow runbook 문서 |
| [08-ai/](./08-ai/README.md) | 08 Ai runbook 문서 |
| [09-tooling/](./09-tooling/README.md) | 09 Tooling runbook 문서 |
| [10-communication/](./10-communication/README.md) | 10 Communication runbook 문서 |
| [11-laboratory/](./11-laboratory/README.md) | 11 Laboratory runbook 문서 |
| [0012-standardize-infra-net.md](./0012-standardize-infra-net.md) | 0012 Standardize Infra Net runbook 문서 |
| [harness-agent-first-engineering-validation.md](./harness-agent-first-engineering-validation.md) | Harness Agent First Engineering Validation runbook 문서 |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md) | Llm Wiki Maintenance runbook 문서 |
| [release-management.md](./release-management.md) | Release Management runbook 문서 |

## Related Documents

- [Operations index](../README.md)
- [Operations Guides](../guides/README.md)
- [Operations Policies](../policies/README.md)
- [Incident records](../incidents/README.md)
