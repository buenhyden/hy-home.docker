# harness-agent-first-engineering Specifications

> 에이전트-퍼스트 엔지니어링 하네스 설계 사양

## Overview

`docs/03.specs/harness-agent-first-engineering`는 Claude/Codex 런타임 하네스, 훅 이벤트 디스패처, 에이전트 카탈로그, 스킬 시스템 설계 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- Repository Maintainers
- AI Agents

## Status

이 사양은 P0–P15 기간에 구현된 하네스 아키텍처의 설계 사양을 보존합니다.

## Scope

### In Scope

- 완료된 agent-first harness 구현 계약 보존
- hook dispatcher, runtime mirror, agent/function catalog 설계 기준
- governance와 runtime surface 간 추적성 링크

### Out of Scope

- 새 agent runtime 기능 구현
- provider-specific runtime 파일 직접 수정 절차
- 실행 계획 또는 작업 evidence 작성

## Structure

```text
harness-agent-first-engineering/
├── spec.md      # Harness architecture specification
└── README.md    # This file
```

## How to Work in This Area

1. 새 작업을 시작하기 전에 [spec.md](./spec.md)에서 harness contract를 확인합니다.
2. runtime 정책 변경은 `docs/00.agent-governance/`와 provider overlays를 함께 확인합니다.
3. 새 harness 변경이 필요하면 이 완료 spec을 덮어쓰지 말고 새 stage artifact로 추적합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [docs/00.agent-governance/README.md](../../00.agent-governance/README.md)
- [.claude/CLAUDE.md](../../../.claude/CLAUDE.md)
