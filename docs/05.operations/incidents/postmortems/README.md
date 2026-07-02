<!-- README Target: docs/05.operations/incidents/postmortems/README.md -->

<!-- Target: docs/05.operations/incidents/postmortems/README.md -->

# 05.operations/incidents/postmortems

> 사고 안정화 이후 사후 분석 문서를 보관하는 공식 postmortem folder

## Overview

이 폴더는 사고 대응이 안정화된 뒤 작성하는 Postmortem 문서를 보관합니다.
Incident 문서는 `docs/05.operations/incidents/YYYY/`에서 사실, 상태, 대응
흐름을 기록하고, Postmortem 문서는 이 폴더에서 근본 원인, 기여 요인,
재발 방지 조치, 검증 항목을 기록합니다.

## Audience

이 README의 주요 독자:

- Operators
- Security Auditors
- Incident Responders
- AI Agents

## Scope

### In Scope

- 사고 안정화 이후의 root-cause analysis
- 기여 요인, 탐지 공백, 재발 방지 조치
- 후속 task, runbook, policy, guardrail, eval 업데이트 링크
- SEV1/SEV2 사고의 필수 사후 분석 기록

### Out of Scope

- 실시간 사고 대응 타임라인
- 복구 절차 본문
- 장기 운영 정책 본문
- secret values, credentials, private keys, raw logs, shell history

## Structure

```text
postmortems/
├── README.md
└── YYYY/
    └── YYYY-MM-DD-incident-title-postmortem.md
```

## How to Work in This Area

1. 새 사후 분석은 [postmortem template](../../../99.templates/templates/operations/postmortem.template.md)을 복사해 시작합니다.
2. paired Incident 문서는 `../../YYYY/YYYY-MM-DD-incident-title.md` 형식으로 연결합니다.
3. 예방 조치는 owner와 verification이 있는 follow-up task 또는 runbook/policy 업데이트로 연결합니다.
4. secret 값, credential, private key, raw log, shell history는 본문에 기록하지 않습니다.
5. 본문은 한국어로 쓰되 timestamp, ID, command, evidence label, service name, environment variable은 원형을 유지합니다.

## Related Documents

- [Incidents index](../README.md)
- [Postmortem template](../../../99.templates/templates/operations/postmortem.template.md)
- [Incident template](../../../99.templates/templates/operations/incident.template.md)
- [Operations index](../../README.md)
- [Runbooks](../../runbooks/README.md)
