# 06.tasks

## 목적

이 폴더는 구현·검증·평가 작업(Task) 단위를 저장한다. 이 폴더의 문서는 단순 TODO가 아니라, Spec과 Plan에서 파생된 실행 가능한 작업 목록의 정본(canonical location)이어야 한다.

## 문서 책임

- 구현 작업 추적
- 검증 및 테스트 작업 추적
- 평가(Eval) 작업 추적
- 작업 증거와 완료 상태 기록

## 포함할 내용

1. Parent Spec 또는 Parent Plan 링크
2. 작업 식별자와 설명
3. 작업 유형
4. 검증 기준과 증거
5. 소유자와 상태
6. 필요 시 테스트 명령, Eval 명령, 로그 위치

## 포함하지 말아야 할 내용

- 전체 시스템 설계 설명
- 운영 정책 정의
- 장애 대응 절차
- 근본 원인 분석

위 내용은 각각 `04.specs/`, `08.operations/`, `09.runbooks/`, `11.postmortems/`로 분리한다.

## 핵심 원칙

1. Task는 상위 Spec 또는 Plan을 참조한다.
2. 핵심 동작은 테스트 우선(TDD)을 기본값으로 한다.
3. Agent 기능은 일반 테스트 외에 Eval을 함께 가진다.
4. 각 Task는 증거(Evidence)와 검증 방법을 포함한다.

## 권장 Task 필드

- Task ID
- Description
- Type (`impl | test | eval | doc | ops`)
- Parent Spec ID / Section
- Parent Plan ID / Phase
- Validation / Evidence
- Owner
- Status

## Agent 전용 Task 타입 예시

- prompt
- tool
- memory
- guardrail
- eval
- observability

## `04.specs`와의 관계

기능 수준에서 밀접한 `tasks.md`는 `04.specs/<feature-id>/`에 둘 수 있다. 그러나 그것은 설계 보조 문서다. 팀 실행용, 스프린트용, 검증 집계용 작업 문서는 `06.tasks/`를 기본 위치이자 정본 위치로 사용한다.

## Templates

- `../99.templates/task.template.md`
