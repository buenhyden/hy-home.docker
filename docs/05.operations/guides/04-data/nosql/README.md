# Operations Guides - 04 Data / Nosql

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides/04-data/nosql`는 `docs/05.operations`의 guide 문서를 관리합니다. 사용 맥락, 전제 조건, 일반 점검, 관련 runbook handoff를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

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
guides/04-data/nosql/
├── cassandra.md
├── couchdb.md
├── mongodb.md
└── README.md
```

## How to Work in This Area

1. 새 문서를 만들기 전에 `docs/99.templates/operation.template.md`의 목적별 profile과 target-relative link 규칙을 확인합니다.
2. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
3. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [cassandra.md](./cassandra.md) | Cassandra guide 문서 |
| [couchdb.md](./couchdb.md) | Couchdb guide 문서 |
| [mongodb.md](./mongodb.md) | Mongodb guide 문서 |

## Related Documents

- [Operations index](../../../README.md)
- [Operations Guides index](../../README.md)
- [Operations Policies - 04-data / nosql](../../../policies/04-data/nosql/README.md)
- [Operations Runbooks - 04-data / nosql](../../../runbooks/04-data/nosql/README.md)
- [Incident records](../../../incidents/README.md)
- [Operations template](../../../../99.templates/operation.template.md)
