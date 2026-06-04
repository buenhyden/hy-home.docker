<!-- README Target: docs/05.operations/runbooks/04-data/relational/README.md -->

# Operations Runbooks - 04 Data / Relational

> 복구, 검증, 반복 실행 절차를 명령과 evidence 중심으로 관리한다.

## Overview

`runbooks/04-data/relational`는 `docs/05.operations`의 relational runbook 문서를 관리한다. 현재는 선택 include인 PostgreSQL HA cluster의 compose 기반 트리거 조건, 순서 있는 점검 절차, evidence, recovery boundary, escalation을 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 한다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- PostgreSQL HA cluster 장애 triage, 정기 점검, escalation, evidence capture
- 현재 경로에 속한 runbook 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 배경 설명 중심 가이드와 장기 운영 정책
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
runbooks/04-data/relational/
├── postgresql-cluster.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [postgresql-cluster.md](./postgresql-cluster.md) | PostgreSQL HA cluster triage runbook |

## Related Documents

- [Operations index](../../../README.md)
- [Operations Runbooks index](../../README.md)
- [Operations Guides - 04-data / relational](../../../guides/04-data/relational/README.md)
- [Operations Policies - 04-data / relational](../../../policies/04-data/relational/README.md)
- [Incident records](../../../incidents/README.md)
