<!-- README Target: docs/05.operations/runbooks/90-knowledge/README.md -->

# Operations Runbooks - 90 Knowledge

> LLM Wiki와 reference 유지보수 반복 실행 절차를 관리한다.

## Overview

`runbooks/90-knowledge`는 `docs/05.operations`의 knowledge maintenance runbook 문서를 관리합니다. generated index freshness, repository map 검증, evidence capture, escalation 기준을 guide/policy와 분리해 둡니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- LLM Wiki maintenance validation, rollback, escalation, evidence capture
- 현재 경로에 속한 runbook 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- source-backed reference 본문 자체
- 배경 설명 중심 가이드와 장기 운영 정책
- secret 값, credential, token, 인증서 원문

## Structure

```text
runbooks/90-knowledge/
├── llm-wiki-maintenance.md
└── README.md
```

## How to Work in This Area

1. knowledge runbook을 추가, 이동, 삭제하면 이 README와 `runbooks/README.md`를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [llm-wiki-maintenance.md](./llm-wiki-maintenance.md) | LLM Wiki maintenance runbook 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Runbooks index](../README.md)
- [Operations Guides - 90-knowledge](../../guides/90-knowledge/README.md)
- [Operations Policies - 90-knowledge](../../policies/90-knowledge/README.md)
- [LLM Wiki references](../../../90.references/llm-wiki/README.md)
