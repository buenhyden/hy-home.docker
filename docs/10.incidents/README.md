# 10.incidents

## 목적

이 폴더는 사고 사실 기록(Incident Record)을 저장한다. Incident는 실시간 또는 최근 종료된 대응 흐름을 기록하는 문서다.

## 문서 책임

- 영향과 상태를 기록한다.
- 타임라인과 대응 조치를 기록한다.
- 증거와 후속 액션을 연결한다.
- 사실과 가설을 구분해 남긴다.

## 포함할 내용

- Incident ID
- 영향 범위
- 타임라인
- 현재 가설
- 대응 및 완화 조치
- 증거
- 후속 액션
- 관련 Runbook / Postmortem 링크

## 포함하지 말아야 할 내용

- 장문의 비난 없는 회고
- 구조적 학습 중심 분석
- 최종 확정 근본 원인 분석

그 내용은 `11.postmortems/`로 분리한다.

## Agent 사고 시 추가 메타데이터

- Model Version
- Prompt Version
- Tool Set / Config
- Guardrail State
- Trace IDs
- Eval Run IDs

## 권장 하위 구조

- `10.incidents/YYYY/YYYY-MM-DD-<incident-title>.md`

## Templates

- `../99.templates/incident.template.md`
