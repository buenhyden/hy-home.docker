# 03.adr

## 목적

이 폴더는 아키텍처 결정 기록(Architecture Decision Record, ADR)을 저장한다. ADR은 중요한 기술·아키텍처 결정 1건을 1문서로 기록한다.

## 포함할 내용

- 맥락(Context)
- 결정(Decision)
- 비목표(Non-goals)
- 대안(Alternatives)
- 결과(Consequences)
- 관련 PRD/ARD/Spec/Plan/기타 ADR 링크

## 포함하지 말아야 할 내용

- 상세 구현 설계
- 운영 절차
- 장문의 제품 배경 설명

## 전역 번호 규칙

ADR은 전역 번호를 사용한다.

- `0001-...`
- `0002-...`

번호는 재사용하지 않는다.

## Agent 관련 ADR 예시

- 모델 선택
- Tool Gating
- Guardrail 전략
- Planner-Executor 채택 여부
- Fallback 모델 정책

## Templates

- `../99.templates/adr.template.md`
