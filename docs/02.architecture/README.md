---
title: "Architecture"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
---

# Architecture

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

`docs/02.architecture`는 Stage 01 요구사항을 시스템 경계, 이해관계자 관심사,
뷰, 데이터·제어 흐름, 품질 시나리오와 중요한 선택으로 연결한다.
Architecture Description은 현재 구조를 설명하고 ADR은 선택, 대안, 근거,
결과와 supersession을 기록한다.

###### Audience
<!-- core-payload-level:4 -->

- System Architects
- Developers
- Reviewers

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 stage는 Architecture Description과 ADR을 보유한다. 개수는 유지 기준이
아니므로 각 하위 디렉터리의 README와 실제 파일 목록이 권위이며 이 index는
그 경로로 안내한다. 구현 세부와 검증 계약은 Stage 03, 실행 상태는 현재 변경
패킷, 운영 절차는 Stage 05가 소유한다.

##### Excluded Responsibilities

구현 세부와 검증 계약은 Stage 03, 실행 상태는 현재 변경 패킷, 운영 절차는 Stage 05가 소유하며 이 stage는 소유하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [01.descriptions/](01.descriptions/README.md) | stakeholder concerns, boundaries, views, flows, quality scenarios, requirement disposition와 관련 결정 |
| [02.decisions/](02.decisions/README.md) | 하나의 material choice, alternatives, rationale, consequences, confirmation과 supersession |

###### Current Items
<!-- core-payload-level:4 -->

```text
docs/02.architecture/
├── 01.descriptions/
├── 02.decisions/
└── README.md
```

###### Current Inventory
<!-- core-payload-level:4 -->

- [`01.descriptions/`](01.descriptions/README.md): stakeholder concerns, boundaries,
  views, flows, quality scenarios, requirement disposition와 관련 결정.
- [`02.decisions/`](02.decisions/README.md): 하나의 material choice, alternatives,
  rationale, consequences, confirmation과 supersession.

###### Classification
<!-- core-payload-level:4 -->

이 stage의 하위 유형은 둘이다. `01.descriptions/`의 Architecture Description은 현재 구조를 설명하는 정본이고 `02.decisions/`의 ADR은 선택과 근거를 기록한다. 비권위 기록용 하위 디렉터리는 없다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`이다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않는다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [Product Requirements](../01.requirements/README.md)
- [Architecture Descriptions](01.descriptions/README.md)
- [Architecture Decisions](02.decisions/README.md)
- [Specifications](../03.specs/README.md)
- [Operations](../05.operations/README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [에이전트 작업 규칙](AGENTS.md)
- [Documentation Templates](../99.templates/README.md)
- [문서 작성 계약](../00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd): README와 AGENTS.md의 역할 구분
- [README 템플릿](../99.templates/02.templates/93.common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Authoring Flow
<!-- core-payload-level:4 -->

1. 상위 [Product Requirements](../01.requirements/README.md)를 확인한다.
2. 새 설명은
   [`description.template.md`](../99.templates/02.templates/02.architecture/description.template.md)를 사용한다.
3. 새 결정은 [`decision.template.md`](../99.templates/02.templates/02.architecture/decision.template.md)를 사용한다.
4. Description은 실제 상위 요구사항, ADR은 실제 Description을
   `parent_ids`로 연결한다.
5. 구현과 운영 사실은 해당 Spec과 Operations 문서에서 확인하고 확인되지
   않은 아키텍처 사실을 만들지 않는다.

###### Documentation Standards
<!-- core-payload-level:4 -->

- Description은 `<4-digit-id>-<slug>.md`, `artifact_id: AD-<4-digit-id>`,
  `type: sdlc/architecture-description`을 일치시킨다.
- ADR은 `<4-digit-id>-<slug>.md`, `artifact_id: ADR-<4-digit-id>`,
  `type: sdlc/architecture-decision`을 일치시킨다.
- 호환·redirect 문서나 병렬 용어 체계를 만들지 않는다.
- 날짜는 경로가 아니라 typed metadata에 둔다.
- View와 diagram은 [공통 Agent 거버넌스 작성 정책](../00.workspace/03.process/documentation-protocol.md#role-specific-authoring)을 적용하고 실제 이해에 필요한 수준만 사용한다.

###### Transition and Exit
<!-- core-payload-level:4 -->

Architecture Description은 draft → in-review → approved로, ADR은 proposed에서 accepted 또는 rejected로 전이한다. 대체되거나 철회된 문서는 현재 소유자에 요약한 뒤 삭제하고 번호를 Registry `reserved_history`에 추가한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
