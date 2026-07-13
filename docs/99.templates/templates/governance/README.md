---
layer: agentic
---

# Governance Templates

## Overview

`docs/99.templates/templates/governance`는 Stage 00 Memory와 Progress 기록,
그리고 전환 중인 harness Task 계약을 위한 복사 가능한 원본을 안내한다.

## Audience

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

- 재사용 가능한 거버넌스 Memory 기록 형식
- 저장소 작업 진행 상황을 기록하는 Progress 형식
- `artifact_type: task`를 유지하는 harness Task 계약 형식

## Structure

| Need | Template |
| --- | --- |
| 문제, 해결, 예방, 증거를 남기는 Memory 기록 | [memory.template.md](./memory.template.md) |
| Stage 00 Progress 구조 작성 | [progress.template.md](./progress.template.md) |
| 보호 경로와 승인·검증 경계를 포함하는 Task 계약 | [harness-task-contract.template.md](./harness-task-contract.template.md) |

## How to Work in This Area

1. Memory와 Progress 대상은 [template selection](../../support/template-selection.md)에서 canonical 원본을 확인한다.
2. 선택한 원본의 모든 토큰을 대상 기록의 실제 내용으로 바꾼다.
3. 사용·보존·검증 규칙은 [Governance Memory](../../../00.agent-governance/memory/README.md)와 support 소유자에서 확인한다.
4. harness Task 전환은 해당 Stage 04 작업의 승인 경계를 따른다.

## Related Documents

- [templates catalog](../README.md)
- [template contract](../../support/template-contract.md)
- [template selection](../../support/template-selection.md)
- [Governance Memory](../../../00.agent-governance/memory/README.md)
