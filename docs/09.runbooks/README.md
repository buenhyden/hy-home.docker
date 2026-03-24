# 09.runbooks

## 목적

이 폴더는 실제 실행 가능한 운영 절차(Runbook)를 저장한다. Runbook은 장문의 배경 설명보다 바로 실행 가능한 순서와 검증 절차를 우선한다.

## 문서 책임

- 특정 상황에서 즉시 수행할 절차 제공
- 검증, 증거 수집, 롤백, 복구를 문서화
- 관련 Incident/Postmortem과 연결

## 포함할 내용

- 목적
- 사용 시점
- 선행 조건
- 절차 또는 체크리스트
- 검증 방법
- 증거 수집 위치
- 롤백/복구 절차
- 에스컬레이션 경로

## 포함하지 말아야 할 내용

- 정책 기준 자체
- 교육용 장문 튜토리얼
- 사고 회고와 근본 원인 분석

위 내용은 각각 `08.operations/`, `07.guides/`, `11.postmortems/`로 분리한다.

## Agent Runbook 예시

- Prompt Rollback
- Model Fallback Switch
- Tool 권한 차단
- Eval 재실행
- Trace 수집

## 연결 규칙

- Canonical Reference로 PRD/ARD/ADR/Spec/Plan을 명시한다.
- 관련 Incident/Postmortem 링크를 둔다.

## 시작 템플릿

- `../99.templates/runbook.template.md`
