<!-- README Target: docs/05.operations/policies/README.md -->

# Operations Policies

> 운영 통제, 보안/가용성 기준, 예외 승인 기준을 관리한다.

## Overview

`policies`는 `docs/05.operations`의 policy 문서를 관리합니다. 필수/허용/금지 상태, 예외 승인, 검증 기준, 검토 주기를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

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

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/
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
├── infra-service-optimization-catalog.md
├── common-optimizations-template-exceptions.md
├── harness-agent-first-engineering.md
├── llm-wiki-maintenance.md
├── 0012-standardize-infra-net.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path                                                                                               | Purpose                                                 |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [01-gateway/](./01-gateway/README.md)                                                              | 01 Gateway policy 문서                                  |
| [02-auth/](./02-auth/README.md)                                                                    | 02 Auth policy 문서                                     |
| [03-security/](./03-security/README.md)                                                            | 03 Security policy 문서                                 |
| [04-data/](./04-data/README.md)                                                                    | 04 Data policy 문서                                     |
| [05-messaging/](./05-messaging/README.md)                                                          | 05 Messaging policy 문서                                |
| [06-observability/](./06-observability/README.md)                                                  | 06 Observability policy 문서                            |
| [07-workflow/](./07-workflow/README.md)                                                            | 07 Workflow policy 문서                                 |
| [08-ai/](./08-ai/README.md)                                                                        | 08 Ai policy 문서                                       |
| [09-tooling/](./09-tooling/README.md)                                                              | 09 Tooling policy 문서                                  |
| [10-communication/](./10-communication/README.md)                                                  | 10 Communication policy 문서                            |
| [11-laboratory/](./11-laboratory/README.md)                                                        | 11 Laboratory policy 문서                               |
| [0012-standardize-infra-net.md](./0012-standardize-infra-net.md)                                   | infra_net IP 관리 policy 문서                           |
| [infra-service-optimization-catalog.md](./infra-service-optimization-catalog.md)             | 12 Infra Service Optimization Catalog policy 문서       |
| [common-optimizations-template-exceptions.md](./common-optimizations-template-exceptions.md) | 13 Common Optimizations Template Exceptions policy 문서 |
| [harness-agent-first-engineering.md](./harness-agent-first-engineering.md)                         | Harness Agent-first Engineering policy 문서             |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md)                                               | LLM Wiki Maintenance policy 문서                        |

## Related Documents

- [Operations index](../README.md)
- [Operations Guides](../guides/README.md)
- [Operations Runbooks](../runbooks/README.md)
- [Incident records](../incidents/README.md)
