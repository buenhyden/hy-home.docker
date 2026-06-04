<!-- README Target: docs/05.operations/guides/90-knowledge/README.md -->

# Operations Guides - 90 Knowledge

> LLM Wiki와 reference 유지보수 guide를 관리한다.

## Overview

`guides/90-knowledge`는 `docs/05.operations`의 knowledge maintenance guide 문서를 관리합니다. LLM Wiki, repository map, generated index freshness처럼 reference stage와 운영 검증 사이를 연결하는 사용 가이드를 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- LLM Wiki와 reference 유지보수 사용 맥락
- 현재 경로에 속한 guide 문서 인덱스
- 관련 policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- source-backed reference 본문 자체
- 운영 통제 기준과 반복 실행 복구 절차
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/90-knowledge/
├── llm-wiki-maintenance.md
└── README.md
```

## How to Work in This Area

1. knowledge guide를 추가, 이동, 삭제하면 이 README와 `guides/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md) | LLM Wiki maintenance guide 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 90-knowledge](../../policies/90-knowledge/README.md)
- [Operations Runbooks - 90-knowledge](../../runbooks/90-knowledge/README.md)
- [LLM Wiki references](../../../90.references/llm-wiki/README.md)
