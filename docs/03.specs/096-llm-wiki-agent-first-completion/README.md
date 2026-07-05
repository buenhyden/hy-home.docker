# llm-wiki-agent-first-completion Specifications

<!-- Target: docs/03.specs/096-llm-wiki-agent-first-completion/README.md -->

> LLM Wiki 에이전트-퍼스트 완성 사양

## Overview

`docs/03.specs/096-llm-wiki-agent-first-completion`는 `docs/90.references/llm-wiki/` 경로 인덱스, `llms.txt` 진입점, LLM Wiki 생성 스크립트 완성 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- Repository Maintainers
- AI Agents

## Status

이 사양은 LLM 탐색 레이어 구축 작업(P0–P15)의 설계 사양을 보존합니다.

## Scope

### In Scope

- 완료된 LLM Wiki generator/index/curator 구현 계약 보존
- repo-local path index, LLM-facing navigation, freshness validation 기준
- LLM Wiki reference와 operations maintenance 링크

### Out of Scope

- public wiki publication
- external model calls or indexing services
- Graphify output as authoritative source

## Structure

```text
llm-wiki-agent-first-completion/
├── spec.md      # LLM wiki completion specification
└── README.md    # This file
```

## How to Work in This Area

1. 새 작업을 시작하기 전에 [spec.md](./spec.md)에서 LLM Wiki contract를 확인합니다.
2. generated index 변경은 `scripts/knowledge/generate-llm-wiki-index.sh --check`로 검증합니다.
3. Graphify는 advisory로만 사용하고 tracked source files와 stage docs로 결론을 확인합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [docs/90.references/llm-wiki/README.md](../../90.references/llm-wiki/README.md)
- [scripts/knowledge/generate-llm-wiki-index.sh](../../../scripts/knowledge/generate-llm-wiki-index.sh)
