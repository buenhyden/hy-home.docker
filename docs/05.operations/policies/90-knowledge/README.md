<!-- README Target: docs/05.operations/policies/90-knowledge/README.md -->

# Operations Policies - 90 Knowledge

> LLM Wiki와 reference 유지보수 통제 기준을 관리한다.

## Overview

`policies/90-knowledge`는 `docs/05.operations`의 knowledge maintenance policy 문서를 관리합니다. LLM Wiki freshness, safety boundary, generated output 검증 기준을 guide/runbook과 분리해 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- knowledge maintenance controls, allowed/disallowed 상태, exception, review cadence
- 현재 경로에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- source-backed reference 본문 자체
- 사용 온보딩과 명령 순서 중심 복구 절차
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/90-knowledge/
├── llm-wiki-maintenance.md
└── README.md
```

## How to Work in This Area

1. knowledge policy를 추가, 이동, 삭제하면 이 README와 `policies/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md) | LLM Wiki maintenance policy 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Policies index](../README.md)
- [Operations Guides - 90-knowledge](../../guides/90-knowledge/README.md)
- [Operations Runbooks - 90-knowledge](../../runbooks/90-knowledge/README.md)
- [LLM Wiki references](../../../90.references/llm-wiki/README.md)
