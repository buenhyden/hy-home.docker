<!-- README Target: docs/05.operations/runbooks/00-workspace/README.md -->

# Operations Runbooks - 00 Workspace

> 서비스 티어 하나에만 속하지 않는 workspace-level 반복 실행 절차를 관리한다.

## Overview

`runbooks/00-workspace`는 `docs/05.operations`의 workspace-level runbook 문서를 관리합니다. harness 검증, LLM Wiki freshness, release readiness처럼 저장소 전체 작업 흐름에 걸친 절차와 evidence capture 기준을 한 곳에 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- workspace-level validation, release readiness, rollback, escalation, evidence capture
- 현재 경로에 속한 runbook 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 배경 설명 중심 가이드와 장기 운영 정책
- 개별 서비스 티어 runbook
- secret 값, credential, token, 인증서 원문

## Structure

```text
runbooks/00-workspace/
├── harness-agent-first-engineering-validation.md
├── llm-wiki-maintenance.md
├── release-management.md
└── README.md
```

## How to Work in This Area

1. workspace-level runbook을 추가, 이동, 삭제하면 이 README와 `runbooks/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [harness-agent-first-engineering-validation.md](./harness-agent-first-engineering-validation.md) | Harness / Agent-first Engineering validation runbook 문서 |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md) | LLM Wiki maintenance runbook 문서 |
| [release-management.md](./release-management.md) | Release management runbook 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Runbooks index](../README.md)
- [Operations Guides - 00-workspace](../../guides/00-workspace/README.md)
- [Operations Policies - 00-workspace](../../policies/00-workspace/README.md)
- [Incident records](../../incidents/README.md)
