---
status: active
---
<!-- Target: docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md -->

# LLM Wiki Maintenance Usage Guide

## Usage

### Overview

이 가이드는 `guides/00-workspace/llm-wiki-maintenance.md` 대상의 사용 맥락, 설정 확인 방법, 안전한 운영 진입점을 설명한다.

이 문서는 LLM Wiki를 언제 확인하거나 갱신해야 하는지 판단할 때 사용한다. 반복 실행 절차는 runbook으로 넘기고, 운영 통제 기준은 policy로 넘긴다.

- Root entrypoints, agent governance docs, operations docs, script inventory, infrastructure indexes, or LLM Wiki files changed.
- A validator reports stale LLM Wiki output.
- An AI agent needs a safe repo-local path index before broader repository exploration.

### Usage Type

`operational-reference | system-guide`

### Target Audience

- Operators
- Developers
- Contributors
- AI Agents

### Purpose

- LLM Wiki Maintenance Usage Guide의 운영 사용 맥락을 빠르게 파악한다.
- 반복 실행 절차와 장애 대응은 연결된 runbook으로 넘긴다.
- 통제 기준은 연결된 policy 문서와 분리해 유지한다.

### Prerequisites

- Repository checkout 접근 가능
- 관련 `docs/03.specs/` 또는 operations 문서 확인 가능
- 필요한 경우 Docker/Docker Compose 명령 실행 권한

### Step-by-step Instructions

1. 이 문서의 overview와 usage context를 확인한다.
2. 관련 service, configuration, 또는 documentation target을 식별한다.
3. `## Common Checks`의 검증 항목을 실행하거나 검토한다.
4. 반복 절차, 장애 대응, rollback, escalation이 필요하면 `## Runbook Handoff`의 runbook으로 이동한다.

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

## Common Checks

- `llms.txt`가 `docs/90.references/llm-wiki/llm-wiki-index.md`와 `repository-map.md`를 가리키는지 확인한다.
- `docs/90.references/llm-wiki/llm-wiki-index.md`가 generated tracked repo-local index인지 확인한다.
- Graphify output은 navigation aid로만 사용하고 source truth로 취급하지 않는다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/00-workspace/llm-wiki-maintenance.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/00-workspace/llm-wiki-maintenance.md)
- [Recovery runbook](../../runbooks/00-workspace/llm-wiki-maintenance.md)
