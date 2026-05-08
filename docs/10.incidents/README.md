# 10.incidents

## 목적

이 폴더는 사고 사실 기록(Incident Record)과 사후 분석(Postmortem)을 저장한다. Incident는 실시간 또는 최근 종료된 대응 흐름을 기록하고, Postmortem은 사고 안정화 이후 구조적 원인과 재발 방지 조치를 기록한다.

## 문서 책임

- 영향과 상태를 기록한다.
- 타임라인과 대응 조치를 기록한다.
- 증거와 후속 액션을 연결한다.
- 사실과 가설을 구분해 남긴다.
- SEV1/SEV2 사고의 구조적 원인, 기여 요인, 재발 방지 조치를 Postmortem으로 남긴다.

## 포함할 내용

- Incident ID
- 영향 범위
- 타임라인
- 현재 가설
- 대응 및 완화 조치
- 증거
- 후속 액션
- 관련 Runbook / Postmortem 링크
- 근본 원인 분석과 재발 방지 조치(Postmortem 문서)

## 포함하지 말아야 할 내용

- 실행 가능한 복구 절차 자체 (Runbook 담당)
- 장기 운영 정책 (Operations 담당)
- 요구사항, 설계, 구현 계획

## Agent 사고 시 추가 메타데이터

- Model Version
- Prompt Version
- Tool Set / Config
- Guardrail State
- Trace IDs
- Eval Run IDs

## 권장 하위 구조

- `10.incidents/YYYY/YYYY-MM-DD-<incident-title>.md`
- `10.incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md`

## Templates

- `../99.templates/incident.template.md`
- `../99.templates/postmortem.template.md`

## Related Documents

- [Runbooks](../09.runbooks/README.md)
- [Operations](../08.operations/README.md)
- [Incident template](../99.templates/incident.template.md)
- [Postmortem template](../99.templates/postmortem.template.md)
