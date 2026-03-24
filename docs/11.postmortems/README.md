# 11.postmortems

## 목적
이 폴더는 사고 사후 분석(Postmortem)을 저장한다. Postmortem은 시스템이 왜 그런 사고를 허용했는지, 무엇을 바꿔야 같은 사고를 줄일 수 있는지를 기록한다.

## 포함할 내용
- 사건 요약
- 영향
- 타임라인
- 근본 원인
- 기여 요인
- 감지 공백
- 액션 아이템
- 재발 방지와 검증
- 관련 Incident / Runbook / ADR / Spec / Operation 링크

## 핵심 원칙
- 비난 없는 분석(Blameless)
- 시스템 중심 원인 분석
- 구체 액션과 소유자 명시
- 문서 체계로의 환류

## Agent 사고 후 권장 환류
- Spec 수정
- Guardrail/Eval 보강
- Operation 정책 보완
- Runbook 갱신
- ADR 추가 또는 갱신

## 권장 하위 구조
- `11.postmortems/2026/YYYY-MM-DD-<slug>.md`

## 시작 템플릿
- `../99.templates/postmortem.template.md`
