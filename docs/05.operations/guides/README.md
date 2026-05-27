<!-- README Target: docs/05.operations/guides/README.md -->

# Operations Guides

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides`는 `docs/05.operations`의 guide 문서를 관리합니다. 사용 맥락, 전제 조건, 일반 점검, 관련 runbook handoff를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 서비스 사용 맥락, 설정 방법, 온보딩, 일반 점검
- 이 bucket에 속한 guide 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 운영 통제 기준과 반복 실행 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/
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
├── developer-setup.md
├── env-key-comparison.md
├── harness-agent-first-engineering.md
├── llm-wiki-maintenance.md
├── sensitive-env-vars-comparison.md
└── README.md
```

## How to Work in This Area

1. 새 문서를 만들기 전에 `docs/99.templates/operation.template.md`의 목적별 profile과 target-relative link 규칙을 확인합니다.
2. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
3. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path                                                                       | Purpose                                    |
| -------------------------------------------------------------------------- | ------------------------------------------ |
| [01-gateway/](./01-gateway/README.md)                                      | 01 Gateway guide 문서                      |
| [02-auth/](./02-auth/README.md)                                            | 02 Auth guide 문서                         |
| [03-security/](./03-security/README.md)                                    | 03 Security guide 문서                     |
| [04-data/](./04-data/README.md)                                            | 04 Data guide 문서                         |
| [05-messaging/](./05-messaging/README.md)                                  | 05 Messaging guide 문서                    |
| [06-observability/](./06-observability/README.md)                          | 06 Observability guide 문서                |
| [07-workflow/](./07-workflow/README.md)                                    | 07 Workflow guide 문서                     |
| [08-ai/](./08-ai/README.md)                                                | 08 Ai guide 문서                           |
| [09-tooling/](./09-tooling/README.md)                                      | 09 Tooling guide 문서                      |
| [10-communication/](./10-communication/README.md)                          | 10 Communication guide 문서                |
| [11-laboratory/](./11-laboratory/README.md)                                | 11 Laboratory guide 문서                   |
| [0012-standardize-infra-net.md](./0012-standardize-infra-net.md)           | infra_net 네트워크 표준화 guide 문서       |
| [developer-setup.md](./developer-setup.md)                                 | Developer Setup guide 문서                 |
| [env-key-comparison.md](./env-key-comparison.md)                           | .env.example vs .env 키 비교 guide 문서    |
| [harness-agent-first-engineering.md](./harness-agent-first-engineering.md) | Harness Agent-first Engineering guide 문서 |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md)                       | LLM Wiki Maintenance guide 문서            |
| [sensitive-env-vars-comparison.md](./sensitive-env-vars-comparison.md)     | Sensitive Env Vars 비교 guide 문서         |

## Related Documents

- [Operations index](../README.md)
- [Operations Policies](../policies/README.md)
- [Operations Runbooks](../runbooks/README.md)
- [Incident records](../incidents/README.md)
- [Operations template](../../99.templates/operation.template.md)
