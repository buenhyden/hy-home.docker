---
title: "Agent Governance Standardization Requirements"
version: "1.1.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "requirements"
artifact_id: "REQ-0024"
parent_ids: []
created: "2026-06-01"
---
# Agent Governance Standardization Requirements

## Problem and Goals

이 저장소의 AI Agent는 provider별 실행 형식이 달라도 하나의 거버넌스와
SDLC를 따라야 한다. 목표는 정책, provider 변환, 문서 형식, 실행 증거의
소유자를 분리하고 `.claude/`, `.codex/`가 독립 정책 소스로
변질되지 않도록 하는 것이다.

## Stakeholders and User Needs

- Maintainer는 충돌 시 어느 문서가 정본인지 즉시 판별할 수 있어야 한다.
- AI Agent는 요청에 필요한 최소 정책, role, skill, Spec, Task만 로드해야 한다.
- Reviewer는 provider projection과 정본의 차이, 승인 경계, 검증 결과를
  재현할 수 있어야 한다.
- Operator는 Agent 작업이 secret, runtime, deployment, remote state로
  확장되지 않도록 명시적인 승인 경계를 필요로 한다.

## Functional Requirements

- **REQ-0024-FR-0001**: `.agents/`는 AI Agent 정책, workflow, canonical role,
  canonical skill, provider boundary의 유일한 규범적 소유자여야 한다.
- **REQ-0024-FR-0002**: 공통 Agent 거버넌스 Provider Registry는 provider identity,
  projection route, model·permission translation, hook binding만 소유하며,
  Stage 99의 문서 profile·path·template 권한을 침범하지 않아야 한다.
- **REQ-0024-FR-0003**: `.claude/`, `.codex/`는 공통 Agent 거버넌스 정본을
  provider 또는 runtime 형식으로 투영하는 adapter여야 하며 별도 정책,
  lifecycle, 완료 기준을 정의해서는 안 된다.
  `.agents/`는 실제 repository-owned 정본이며 governance, role, 호출 가능한
  skill만 등록된 경로에 둔다. Native provider 문서는 각 `.claude/`와 `.codex/`의
  작성 원본으로 유지하고, 생성된 README나 adapter가 정본을 덮어쓰지 않아야 한다.
  Codex는 정본 skill을 검색하고 명시적으로 읽으며, Claude는 정본으로 연결하는
  얇은 생성 adapter를 사용한다. 두 provider의 skill은 명시적으로 호출하고,
  discovery·loading·invocation·runtime acceptance를 같은 증거로 주장하지 않는다.
  알 수 없거나 안전하지 않은 내용은 fail closed로 보존하며 자동 삭제하지 않는다.
- **REQ-0024-FR-0004**: canonical role과 skill은 `.agents/`에 한 번만 정의되고,
  생성·추적되는 provider surface는 이름, 역할, scope, source 관계를 보존해야
  한다.
- **REQ-0024-FR-0005**: repository 변경을 수행하는 Agent는 bootstrap policy와
  provider adapter를 거쳐 관련 Requirement, Architecture, active Spec과 current
  Task를 로드해야 한다.
- **REQ-0024-FR-0006**: SDLC는 Requirement → Architecture/ADR → Spec →
  implementation → Operations의 단일 흐름을 사용하고, 실행 상태와 증거는
  현재 Spec Package의 Task가 소유해야 한다.
- **REQ-0024-FR-0007**: 일반 완료 판단은 검토된 diff, 등록된 검증 결과,
  current Task evidence로 이루어져야 하며 branch SHA 고정, corpus snapshot,
  병렬 handoff ledger를 별도 완료 조건으로 요구해서는 안 된다.
- **REQ-0024-FR-0008**: governance Gate와 fixture는 Stage 99 Registry,
  script manifest, workflow contract가 선언한 현재 계약만 검사하고 폐기된
  경로·문서 본문·고정 파일 수를 재현해서는 안 된다.

## Non-functional Requirements

- **REQ-0024-NFR-0009**: 규칙 해석과 provider projection 검증은 결정적이고
  상충하는 fallback 없이 fail closed해야 한다.
- **REQ-0024-NFR-0010**: `.agents/`는 English-only를 유지하고 provider adapter는
  의미를 손실하지 않아야 한다.
- **REQ-0024-NFR-0011**: Agent 권한은 최소 범위여야 하며 secret, credential,
  private key, token 또는 승인되지 않은 외부 상태를 노출하거나 변경해서는
  안 된다.
- **REQ-0024-NFR-0012**: 검증 실패는 소유자와 수정 대상을 식별할 수 있어야
  하며 중복 aggregate Gate가 같은 predicate를 여러 번 소유해서는 안 된다.
- **REQ-0024-NFR-0013**: current 문서는 추적된 구현과 일치해야 하고,
  Legacy·Deprecated·상충 규칙은 current surface에서 제거되어야 한다.

## Constraints

- 공통 Agent 거버넌스 정책 변경은 승인된 repository 범위 안에서만 수행한다.
- Provider adapter는 user-global 설정이나 credential을 정본 입력으로 사용하지
  않는다.
- Historical body clone, compatibility redirect, 별도 progress document를 만들지
  않는다.
- Runtime, deployment, secret, remote GitHub 상태 변경은 별도 명시 승인이
  필요하다.

## Acceptance Criteria

- 공통 Agent 거버넌스와 provider surface 사이에 이름·source·scope drift가 없다.
- `.claude/`, `.codex/`의 tracked 파일이 Provider Registry가 허용한
  작성된 provider adapter, 생성 projection 또는 native runtime mechanics로 분류된다.
- canonical skill의 native entry와 중첩 governance metadata가 동일한 ID·owner·scope를 보존하며, 명시적 호출 설정은 권한을 확대하지 않는다.
- active Task의 Spec/Plan parent가 모두 active이며 terminal parent에 active
  child가 없다.
- 등록된 governance와 document suites가 중복 predicate나 historical fixture
  의존 없이 통과한다.
- current authority가 Stage 98 문서나 삭제된 실행 ledger를 입력으로 사용하지
  않는다.

## Traceability

- **Architecture Description**: [AD-0027 Agent Governance Canonical Adapter](../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- **Decision**: [ADR-0032 Canonical Agent Governance Home](../02.architecture/decisions/0032-canonical-agent-governance-home.md)
- **Historical implementation evidence**: [SPEC-0158](../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md)
- **Governance entry**: [canonical agent governance](../../.agents/README.md)
