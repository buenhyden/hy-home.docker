# 04.specs

## 목적

이 폴더는 설계 명세(Specification)의 중심이다. SDD(Software Design Description) 관점에서 기능, 서비스, API, 데이터 모델, AI Agent 설계를 구체화한다.

## 문서 책임

- 기능 또는 서비스의 기술 설계
- 인터페이스와 데이터 계약
- 비기능 요구와 운영성
- AI Agent 역할, 도구, 평가, 안전 제약
- API 계약 문서의 부모 위치

## 포함할 내용

- 설계 범위와 비목표
- 관련 PRD / ARD / ADR 입력 링크
- 핵심 설계
- 데이터 모델
- 인터페이스와 계약
- Verification
- 필요 시 API Spec, Agent 설계, 계약 파일

## 포함하지 말아야 할 내용

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- 실행 추적의 정본 작업 목록

위 내용은 각각 `01.prd/`, `08.operations/`, `09.runbooks/`, `06.tasks/`로 분리한다.

## 권장 내부 구조

```text
04.specs/
  001-feature-name/
    spec.md
    api-spec.md
    agent-design.md
    data-model.md
    tests.md
    contracts/
      openapi.yaml
```

## 기본 문서 역할

- `spec.md`: 기능 전체 설계, 계약, 비기능 요구, 검증 기준
- `api-spec.md`: API 계약 상세
- `agent-design.md`: Agent 역할, 도구, 메모리, 정책, 오케스트레이션
- `data-model.md`: 데이터 구조와 저장 전략
- `tests.md`: TDD 기반 테스트 전략, 테스트 케이스, 평가 항목
- `contracts/`: OpenAPI, gRPC proto, GraphQL schema 등 기계 가독 계약 파일

## API Specifications

이 디렉터리의 기능 또는 서비스 Spec 중 API 계약이 필요한 경우, 별도의 API Spec 문서를 사용한다.

- 위치 예시:
  - `docs/04.specs/<feature-id>/api-spec.md`
- 사용 템플릿:
  - `docs/99.templates/api-spec.template.md`

### 역할 구분

- 메인 Spec:
  - 기능/서비스 전체 설계, 데이터 모델, 비기능 요구, 운영성, 관측성을 다룬다.
- API Spec:
  - HTTP/GraphQL/gRPC 계약, 엔드포인트, 스키마, 인증, 에러, 버저닝, 거버넌스를 상세히 정의한다.

### 금지 규칙

- API Spec을 `docs/api/` 같은 별도 최상위 문서 체계로 분리하지 않는다.
- API Spec은 `04.specs` 아래 기능 단위 하위 문서로 유지한다.

## Spec 작성 규칙

1. 모든 활성 Spec은 관련 PRD와 ARD를 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Criteria와 테스트는 PRD에서 이어지고, 구현 검증은 Task와 연결된다.
4. API가 있다면 API Spec 또는 계약 파일을 함께 둔다.
5. Agent 설계가 있다면 아래 항목을 명시한다.
   - Agent Role & IO Contract
   - Tools & Tool Contract
   - Prompt/Policy Contract
   - Memory & Context Strategy
   - Guardrails
   - Evaluation
   - Failure Modes / Fallback / Human Escalation

## `06.tasks`와의 관계

- 기능 내부의 설계 보조용 `tasks.md` 또는 `tests.md`는 `04.specs/<feature-id>/`에 둘 수 있다.
- 그러나 실행 추적, 스프린트 관리, 검증·평가 기록의 정본은 `06.tasks/`에 둔다.

## Specifications

이 디렉터리는 인프라 각 계층(Tier) 및 핵심 기능에 대한 상세 기술 명세를 관리한다.

- [01-gateway](./01-gateway/spec.md)
- [02-auth](./02-auth/spec.md) (updated: 2026-03-28 optimization hardening)
- [03-security](./03-security/spec.md) (updated: 2026-03-28 optimization hardening)
- [04-data](./04-data/spec.md) (updated: 2026-03-28 optimization hardening)
- [05-messaging](./05-messaging/spec.md) (updated: 2026-03-28 optimization hardening)
- [06-observability](./06-observability/spec.md) (updated: 2026-03-28 optimization hardening)
- [07-workflow](./07-workflow/spec.md) (updated: 2026-03-28 optimization hardening)
- [08-ai](./08-ai/spec.md) (updated: 2026-03-28 optimization hardening)
- [09-tooling](./09-tooling/spec.md) (updated: 2026-03-28 optimization hardening)
- [11-laboratory](./11-laboratory/spec.md) (updated: 2026-03-28 optimization hardening)

## Templates

- `../99.templates/spec.template.md`
- `../99.templates/api-spec.template.md`
- `../99.templates/agent-design.template.md`
- `../99.templates/data-model.template.md`
- `../99.templates/tests.template.md`
- `../99.templates/openapi.template.yaml`
- `../99.templates/service.template.proto`
- `../99.templates/schema.template.graphql`
