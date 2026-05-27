<!-- README Target: docs/05.operations/incidents/README.md -->

<!-- Target: docs/05.operations/incidents/README.md -->

# 05.operations/incidents

> 사고 기록과 사후 분석을 보관하는 공식 incident stage

## Overview

이 폴더는 사고 사실 기록(Incident Record)과 사후 분석(Postmortem)을 저장합니다. Incident는 실시간 또는 최근 종료된 대응 흐름을 기록하고, Postmortem은 사고 안정화 이후 구조적 원인과 재발 방지 조치를 기록합니다.

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

### Out of Scope

- 실행 가능한 복구 절차 자체 (Runbook 담당)
- 장기 운영 정책 (Operations 담당)
- 요구사항, 설계, 구현 계획

## Structure

```text
05.operations/incidents/
├── YYYY/
│   ├── date-slug incident record
│   └── date-slug postmortem record
└── README.md
```

## How to Work in This Area

1. 새 사고 기록은 [incident template](../../99.templates/incident.template.md)을 복사해 시작합니다.
2. 새 사후 분석은 [postmortem template](../../99.templates/postmortem.template.md)을 복사해 시작합니다.
3. 사고 대응 절차는 이 폴더에 직접 쓰지 말고 관련 runbook으로 연결합니다.
4. 사실, 가설, 조치, 후속 액션을 분리해서 기록하고 관련 증거 링크를 남깁니다.

## Templates

- [incident.template.md](../../99.templates/incident.template.md)
- [postmortem.template.md](../../99.templates/postmortem.template.md)

## Related Documents

- [Operations index](../README.md)
- [Runbooks](../runbooks/README.md)
- [Incident template](../../99.templates/incident.template.md)
- [Postmortem template](../../99.templates/postmortem.template.md)
