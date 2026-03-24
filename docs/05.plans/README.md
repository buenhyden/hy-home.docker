# 05.plans

## 목적

이 폴더는 실행 계획(Plan)을 저장한다. Plan은 언제, 누가, 어떤 순서로, 어떤 제약과 위험을 관리하며 작업을 진행하는지 정의한다.

## 포함할 내용

- 목표와 범위
- 단계(Phase) 또는 추적 표
- 위험과 완화 전략
- 검증 게이트
- 완료 기준
- 롤아웃/롤백 전략

## AI Agent 계획에 추가할 내용

- Offline Eval 통과 기준
- Canary/Sandbox Rollout
- Human Approval Gate
- Prompt/Model 버전 승격 기준
- Rollback 조건

## 연결 규칙

- Plan은 PRD/ARD/Spec/ADR를 참조한다.
- Task는 Plan의 단계 또는 Task ID를 상위 참조로 가진다.

## 시작 템플릿

- `../99.templates/plan.template.md`
