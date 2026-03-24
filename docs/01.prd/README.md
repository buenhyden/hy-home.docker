# 01.prd

## 목적

이 폴더는 제품 요구사항(Product Requirements Document, PRD)을 저장한다. PRD는 무엇을 왜 만들어야 하는지, 누구를 위한 기능인지, 어떤 성공 기준을 만족해야 하는지를 정의한다.

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

## 권장 파일명

- `YYYY-MM-DD-<feature-or-system>.md`

## Templates

- `../99.templates/prd.template.md`
