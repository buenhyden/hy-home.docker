<!-- README Target: docs/05.operations/guides/04-data/README.md -->

# Operations Guides - 04 Data

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides/04-data`는 `docs/05.operations`의 guide 문서를 관리합니다. 사용 맥락, 전제 조건, 일반 점검, 관련 runbook handoff를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 서비스 사용 맥락, 설정 방법, 온보딩, 일반 점검
- 현재 경로에 속한 guide 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 운영 통제 기준과 반복 실행 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/04-data/
├── analytics/
├── cache-and-kv/
├── lake-and-object/
├── nosql/
├── operational/
├── optimization/
├── relational/
├── specialized/
└── README.md
```

> **참고**: `04-data` 가이드는 다른 tier와 달리 카테고리 서브폴더 구조를 사용한다.
> 데이터 tier가 `analytics/`, `cache-and-kv/`, `lake-and-object/`, `nosql/`,
> `operational/`, `relational/`, `specialized/` 등 이질적인 서비스를 12개 이상 포함하기 때문이다.
> 다른 tier는 서비스 수가 적어 flat 구조를 유지한다. 이 비대칭 구조는 의도적이며 거버넌스에서 허용된다.
> (`docs/00.agent-governance/rules/documentation-protocol.md` Section 7 참조)

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path                                                     | Purpose                           |
| -------------------------------------------------------- | --------------------------------- |
| [analytics/](./analytics/README.md)                      | Analytics guide 문서              |
| [cache-and-kv/](./cache-and-kv/README.md)                | Cache And Kv guide 문서           |
| [lake-and-object/](./lake-and-object/README.md)          | Lake And Object guide 문서        |
| [nosql/](./nosql/README.md)                              | Nosql guide 문서                  |
| [operational/](./operational/README.md)                  | Operational guide 문서            |
| [optimization/](./optimization/README.md)                | Optimization guide 문서           |
| [relational/](./relational/README.md)                    | Relational guide 문서             |
| [specialized/](./specialized/README.md)                  | Specialized guide 문서            |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 04-data](../../policies/04-data/README.md)
- [Operations Runbooks - 04-data](../../runbooks/04-data/README.md)
- [Incident records](../../incidents/README.md)
