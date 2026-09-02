---
title: Operations Templates
version: 1.0.0
type: common/readme
owner: "@buenhyden"
---

# Operations Templates

## Overview

이 디렉터리는 Stage 05의 사용 안내, 운영 통제, 실행 절차, 사고 대응,
회고를 위한 복사 가능 양식을 제공한다. 역할과 경로
선택 규칙은 이 카탈로그가 아니라 Stage 99 Registry가 소유한다.

## Audience

- Documentation Writers
- Operations/SRE Engineers
- Incident Responders
- AI Agents

## Scope

이 카탈로그는 다섯 Operations 양식의 위치와 역할만 안내한다. 메타데이터,
선택, lifecycle, 승인, 이관 및 검증 규칙은 support 문서를 따른다.

새 Guide, Policy, Runbook은 역할별 병렬 root가 아니라
`docs/05.operations/catalog/<domain>/####-<subject>/`에 함께 둔다. 기존 역할이
없는 subject에 새 문서를 만들려면 별도 승인과 inventory 근거가 필요하다.

## Structure

| 역할 | 양식 |
| --- | --- |
| 일상 사용 맥락과 공통 점검 | [guide.template.md](./guide.template.md) |
| 필수·금지 통제와 예외 | [policy.template.md](./policy.template.md) |
| 순서화된 절차, 증거, 복구, escalation | [runbook.template.md](./runbook.template.md) |
| 사고 영향, 시간선, 대응 상태 | [incident.template.md](./incident.template.md) |
| 원인, 교훈, 재발 방지 조치 | [postmortem.template.md](./postmortem.template.md) |

Operations subject navigation은 Stage root와 13개 domain `README.md`만
발행한다. subject 폴더에는 `README.md`를 만들지 않으며, incident는 catalog의
sibling인 stable event 경로와 전용 인덱스를 사용한다.

## How to Work in This Area

1. [Stage 99 Registry](../../registry.json)에서 문서 목적과
   대상 경로를 확인한다.
2. 해당 양식을 복사하고 모든 토큰을 주제별 근거로 교체한다.
3. [Stage 99 contract](../../README.md)와 활성 co-located
   Task에 검증 및 검토 증거를 기록한다.
4. Guide의 `## Runbook Handoff`는 실제 sibling Runbook으로 넘길 때만,
   Runbook의 `## Automation Handoff`는 실제 automation artifact와 검증 가능한
   link가 있을 때만 추가한다.

## Related Documents

- [templates catalog](../README.md)
- [Stage 99 Registry](../../registry.json)
- [Stage 99 contract](../../README.md)
