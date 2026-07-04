<!-- README Target: docs/05.operations/guides/00-workspace/README.md -->

# Operations Guides - 00 Workspace

> 서비스 티어 하나에만 속하지 않는 workspace-level 사용, 설정, 온보딩 guide를 관리한다.

## Overview

`guides/00-workspace`는 `docs/05.operations`의 workspace-level guide 문서를 관리합니다. 로컬 개발 준비, env/secrets metadata 비교, agent-first 운영 맥락, LLM Wiki maintenance, 신규 서비스 온보딩처럼 특정 서비스 leaf보다 저장소 전체 운영 흐름에 가까운 사용 가이드를 한 곳에 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 저장소 전체에 적용되는 사용 맥락, 설정 방법, 온보딩, 일반 점검
- 현재 경로에 속한 guide 문서 인덱스
- 관련 workspace policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 개별 서비스 티어 guide
- 운영 통제 기준과 반복 실행 복구 절차
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/00-workspace/
├── developer-setup.md
├── env-key-comparison.md
├── harness-agent-first-engineering.md
├── llm-wiki-maintenance.md
├── new-service-onboarding.md
├── sensitive-env-vars-comparison.md
└── README.md
```

## How to Work in This Area

1. workspace-level guide를 추가, 이동, 삭제하면 이 README와 `guides/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [developer-setup.md](./developer-setup.md) | Developer setup guide 문서 |
| [env-key-comparison.md](./env-key-comparison.md) | `.env.example` vs `.env` metadata comparison guide 문서 |
| [harness-agent-first-engineering.md](./harness-agent-first-engineering.md) | Harness / Agent-first Engineering guide 문서 |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md) | LLM Wiki maintenance guide 문서 |
| [new-service-onboarding.md](./new-service-onboarding.md) | New service onboarding guide 문서 |
| [sensitive-env-vars-comparison.md](./sensitive-env-vars-comparison.md) | Sensitive env vars metadata comparison guide 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 00-workspace](../../policies/00-workspace/README.md)
- [Operations Runbooks - 00-workspace](../../runbooks/00-workspace/README.md)
- [Incident records](../../incidents/README.md)
