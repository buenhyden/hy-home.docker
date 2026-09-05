---
title: "05.operations/incidents"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "operations"
---

<!-- README Target: docs/05.operations/incidents/README.md -->

<!-- Target: docs/05.operations/incidents/README.md -->

# 05.operations/incidents

> 사고 기록과 사후 분석을 보관하는 공식 incident stage

## Overview

이 폴더는 사고 사실 기록(Incident Record)과 사후 분석(Postmortem)을
저장합니다. Incident는 실시간 또는 최근 종료된 대응 흐름을 기록하고,
Postmortem은 사고 안정화 이후 구조적 원인과 재발 방지 조치를 기록합니다.
사고 서술은 한국어를 기본으로 하되 timestamps, IDs, commands, evidence labels,
service names, environment variables는 원형을 유지합니다.

## Audience

이 README의 주요 독자:

- Operators
- Security Auditors
- Incident Responders
- AI Agents

## Scope

### In Scope

- Incident ID, 영향 범위, 상태, 타임라인
- 현재 가설, 대응 및 완화 조치, 증거
- 후속 액션과 관련 Runbook / Postmortem 링크
- SEV1/SEV2 사고의 구조적 원인, 기여 요인, 재발 방지 조치
- Agent 사고의 model, prompt, tool, guardrail, trace, eval metadata
- 사람이 읽는 한국어 사고 서술과 원형을 유지해야 하는 timestamp, ID,
  command, evidence label, service name, environment variable

### Out of Scope

- 실행 가능한 복구 절차 자체 (Runbook 담당)
- 장기 운영 정책 (Operations 담당)
- 요구사항, 설계, 구현 계획

## Structure

```text
05.operations/incidents/
├── YYYY/
│   └── inc-####-<slug>/
│       ├── incident.md
│       └── postmortem.md
└── README.md
```

> **현황 (2026-05-28)**: 기록된 사고가 없어 `YYYY/` 연도 폴더가 존재하지 않는다.
> 첫 사고 발생 시 `incidents/2026/inc-####-<slug>/` 폴더를 생성하고,
> 사고 기록과 사후 분석을 같은 incident packet 안에 저장한다.

### Templates

- [incident.template.md](../../99.templates/templates/operations/incident.template.md)
- [postmortem.template.md](../../99.templates/templates/operations/postmortem.template.md)

## How to Work in This Area

1. 새 사고는 `docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md`
   경로에서 시작합니다.
2. 사고 기록은 [incident template](../../99.templates/templates/operations/incident.template.md)을 복사해 `incident.md`로 작성합니다.
3. 사후 분석은 [postmortem template](../../99.templates/templates/operations/postmortem.template.md)을 복사해 `docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md`로 작성합니다.
4. Postmortem은 자신의 등록된 stable ID를 가지며 `parent_ids`로 해당
   Incident를 연결합니다. Severity와 affected service는 body의 `Impact`에
   기록하고 Registry에 없는 frontmatter key를 추가하지 않습니다.
5. 사고 대응 절차는 이 폴더에 직접 쓰지 말고 관련 runbook으로 연결합니다.
6. 사실, 가설, 조치, 후속 액션을 분리해서 기록하고 관련 증거 링크를 남깁니다.
7. 본문은 한국어로 쓰되 timestamp, ID, command, evidence label, service name,
   environment variable은 원형을 유지합니다.
8. [Stage 00 작성 정책](../../00.agent-governance/policies/documentation-protocol.md#role-specific-authoring)에
   따라 UTC offset을 포함한 ISO 8601 timestamp를 사용하고, 사실과 가설을
   구분합니다. Postmortem은 blameless 서술을 사용하며 각 corrective action에
   owner, due date, tracking ID/link, verification 조건을 기록합니다.

## Related Documents

- [Operations index](../README.md)
- [Runbooks](../README.md)
- [Incident template](../../99.templates/templates/operations/incident.template.md)
- [Postmortem template](../../99.templates/templates/operations/postmortem.template.md)
