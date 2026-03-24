# docs/ 문서 체계 안내

## 목적

이 디렉터리는 제품 요구(Product Requirements), 아키텍처 요구(Architecture Requirements), 결정 기록(Architecture Decision Record), 설계 명세(Specification), 실행 계획(Plan), 구현·검증 작업(Task), 운영 정책(Operations), 실행 절차(Runbook), 사고 기록(Incident), 사후 분석(Postmortem)을 한 흐름으로 관리하기 위한 표준 문서 공간이다.

이 체계는 다음 세 가지를 동시에 만족하도록 설계한다.

1. SDD(Software Design Description) 기반으로 요구-설계-결정을 추적한다.
2. TDD(Test-Driven Development) 기반으로 검증 가능한 구현과 작업 단위를 관리한다.
3. AI Agent 설계와 운영을 일반 소프트웨어 문서 체계 안에 통합한다.

## 문서 흐름

기본 흐름은 아래와 같다.

`01.prd → 02.ard → 03.adr → 04.specs → 05.plans → 06.tasks → 07.guides / 08.operations / 09.runbooks → 10.incidents → 11.postmortems`

보조 문서는 다음과 같다.

- `90.references/`: 느리게 변하는 기준 정보, 용어집, 외부 표준 요약
- `99.templates/`: 새 문서를 시작할 때 반드시 복사해 쓰는 템플릿

## 최상위 폴더 역할

- `01.prd/`: 제품·기능 요구와 성공 기준
- `02.ard/`: 시스템 수준 요구, 품질 속성, 경계, 참조 아키텍처
- `03.adr/`: 중요한 기술·아키텍처 결정 1건당 1문서
- `04.specs/`: 기능·서비스·AI Agent 설계 명세의 중심
- `05.plans/`: 실행, 롤아웃, 마이그레이션, 실험 계획
- `06.tasks/`: 구현·검증·평가 작업 단위의 정본 위치
- `07.guides/`: 온보딩, how-to, 사용 가이드
- `08.operations/`: 공통 운영 정책, 기준, 통제
- `09.runbooks/`: 실제 실행 가능한 절차
- `10.incidents/`: 사고 사실 기록과 대응 로그
- `11.postmortems/`: 원인 분석과 재발 방지 학습
- `90.references/`: 기준 지식과 참고 문서
- `99.templates/`: 문서 템플릿

## 공통 작성 규칙

1. 문서 한 개는 역할 하나만 가진다.
2. 상대 경로(Relative Link)만 사용한다.
3. 상위 문서와 하위 문서의 연결을 명시한다.
4. Placeholder는 저장 전에 모두 제거한다.
5. 결정은 ADR에, 상세 설계는 Spec에, 절차는 Runbook에 둔다.
6. Incident는 사실 기록에 집중하고, Postmortem은 구조적 학습에 집중한다.
7. AI Agent 관련 변경은 설계(Spec), 계획(Plan), 평가(Task/Eval), 운영 정책(Operation), 절차(Runbook)까지 연결되어야 한다.

## README에 반드시 들어가야 하는 내용

각 하위 폴더의 `README.md`는 최소한 아래 항목을 설명해야 한다.

1. 목적
2. 문서 책임
3. 포함할 내용
4. 포함하지 말아야 할 내용
5. 상위/하위 문서 관계
6. 배치 규칙
7. 시작 템플릿

## 추천 내부 배치 규칙

### Feature 단위

기능 또는 서비스는 `04.specs/<feature-id>/` 아래에 설계 중심 파일을 둔다.

예시:

```text
04.specs/
  001-agent-orchestrator/
    spec.md
    api-spec.md
    agent-design.md
    data-model.md
    tests.md
    contracts/
      openapi.yaml
```

### Plan과 Task의 위치

- 기능 내부 설계와 강하게 결합된 계획·작업 초안은 `04.specs/<feature-id>/` 아래에 둘 수 있다.
- 여러 기능을 가로지르는 롤아웃·이행 계획은 `05.plans/`에 둔다.
- 실제 실행용 작업 목록, 스프린트 작업, 검증·평가 실행 기록의 정본(canonical location)은 `06.tasks/`에 둔다.

## API Specification 처리 원칙

API 계약이 필요한 기능은 `spec.md`만으로 끝내지 않는다.

- 메인 Spec: 기능 전체 설계, 데이터 모델, 비기능 요구, 운영성
- API Spec: HTTP/GraphQL/gRPC 계약, 인증, 에러, 버전, 스키마
- 기계 가독 계약 파일: `openapi.yaml`, `.proto`, `schema.graphql`

권장 위치:

- `docs/04.specs/<feature-id>/api-spec.md`
- 템플릿: `docs/99.templates/api-spec.template.md`

금지 규칙:

- `docs/api/` 같은 별도 최상위 API 문서 체계를 만들지 않는다.
- API Spec은 `04.specs/`의 하위 문서로 유지한다.

## AI Agent 문서 원칙

AI Agent 관련 기능은 일반 소프트웨어 설계와 동일한 흐름을 따르되, 아래 항목을 반드시 고려한다.

- Agent 역할(Role)과 입력/출력 계약(IO Contract)
- Tool 계약(Tool Contract)과 권한 범위
- Prompt/Policy 계약
- Memory/Context 전략
- Guardrail
- Evaluation(Eval) 기준과 데이터셋
- Failure Mode, Fallback, Human Escalation
- 운영 정책과 사고 대응 절차

## 문서 생성 시작점

새 문서는 항상 `99.templates/`에서 시작한다.

권장 순서:

1. PRD 작성
2. ARD 작성 또는 기존 ARD 연결
3. ADR 필요 여부 판단
4. Spec 작성
5. API가 있으면 API Spec 추가
6. Plan 작성
7. Task 작성
8. Guide / Operation / Runbook 필요 여부 판단
9. 사고 발생 시 Incident, 종료 후 Postmortem 작성
