---
status: active
---
<!-- Target: docs/05.operations/guides/llm-wiki-maintenance.md -->

# LLM Wiki Maintenance Usage Guide

## Overview (KR)

이 가이드는 `guides/llm-wiki-maintenance.md` 대상의 사용 맥락, 설정 확인 방법, 안전한 운영 진입점을 설명한다.

## Usage

이 문서는 LLM Wiki를 언제 확인하거나 갱신해야 하는지 판단할 때 사용한다. 반복 실행 절차는 runbook으로 넘기고, 운영 통제 기준은 policy로 넘긴다.

- Root entrypoints, agent governance docs, operations docs, script inventory, infrastructure indexes, or LLM Wiki files changed.
- A validator reports stale LLM Wiki output.
- An AI agent needs a safe repo-local path index before broader repository exploration.

## Common Checks

- `llms.txt`가 `docs/90.references/llm-wiki/index.md`와 `repository-map.md`를 가리키는지 확인한다.
- `docs/90.references/llm-wiki/index.md`가 generated tracked repo-local index인지 확인한다.
- Graphify output은 navigation aid로만 사용하고 source truth로 취급하지 않는다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/llm-wiki-maintenance.md)을 따른다.

## Related Documents

- [Operations index](../README.md)
- [Operations policy](../policies/llm-wiki-maintenance.md)
- [Recovery runbook](../runbooks/llm-wiki-maintenance.md)
- [Operations template](../../99.templates/operation.template.md)
