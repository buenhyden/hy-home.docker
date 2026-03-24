# 01. PRD (Product Requirements)

## 목적

제품의 목표, 사용자 가치, 그리고 성공 기준을 정의한 문서다.
모든 개발의 시작점이며, '무엇을(What)', '왜(Why)' 개발하는지 설명한다.

## 포함할 내용

- 문제 정의
- 사용자/운영자 가치
- 기능 요구
- 성공 지표
- 수용 기준(Acceptance Criteria)
- 범위(In Scope)와 비범위(Out of Scope)

## 포함하지 말아야 할 내용

- 상세 구현 방법
- 구체 기술 스택 선택
- 개별 파일 수준 설계
- 장애 대응 절차

위 내용은 각각 `02.ard/`, `03.adr/`, `04.specs/`, `09.runbooks/`로 분리한다.

## 연결 규칙

- PRD는 관련 ARD, Spec, Plan 링크를 가진다.
- Spec은 PRD 요구 ID를 추적한다.
- Agent 기능인 경우 사용 시나리오, 허용/금지 행동, human-in-the-loop 요구를 포함한다.


## Templates

- `../99.templates/prd.template.md`
