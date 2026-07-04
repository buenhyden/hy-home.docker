<!-- README Target: docs/05.operations/guides/07-workflow/README.md -->

# Operations Guides - 07 Workflow

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides/07-workflow`는 `docs/05.operations`의 guide 문서를 관리합니다. 사용 맥락, 전제 조건, 일반 점검, 관련 runbook handoff를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.
현재 active guide는 구현된 Airflow와 n8n 서비스만 다루며, 중복되거나 구현 경로와 상충하는 guide는 `docs/98.archive` tombstone으로 이동한다.

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
guides/07-workflow/
├── airflow-dag-basics.md
├── airflow.md
├── n8n.md
├── optimization-hardening.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [airflow-dag-basics.md](./airflow-dag-basics.md) | Airflow DAG 작성 위치와 기본 패턴 |
| [airflow.md](./airflow.md) | Airflow runtime, access, common checks |
| [n8n.md](./n8n.md) | n8n runtime, workflow 작성, access, queue-mode common checks |
| [optimization-hardening.md](./optimization-hardening.md) | workflow hardening 변경 절차와 검증 기준 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 07-workflow](../../policies/07-workflow/README.md)
- [Operations Runbooks - 07-workflow](../../runbooks/07-workflow/README.md)
- [Incident records](../../incidents/README.md)
