---
title: "Requirement Packages"
version: "1.1.9"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "requirements"
---

# Requirement Packages

## Stage Responsibility

### Purpose and Readers

`docs/01.requirements`는 제품의 문제, 이해관계자 가치, 범위, 요구사항과
수용 기준을 하나의 Requirement Package로 관리한다. 구현 구조는 Stage 02와
Stage 03, 실행 증거는 Stage 03 Spec Package의 현재 Task, 운영 절차는 Stage 05가 소유한다.

#### Audience

- Product Owners
- System Architects
- Developers

### Inputs and Outputs

이 디렉터리는 현재 Requirement Package를 관리한다. 각 패키지는
functional, quality(non-functional) 요구사항을 같은 경계에서 관리하고,
solution-independent interface 요구는 functional 요구사항으로 쓴다. 별도 역할 문서를 병렬로 만들지 않는다. 아래 색인은 현재 패키지를
안내하며, 패키지가 추가·변경·삭제되면 같은 변경에서 갱신한다.

Requirement Package는 문제와 이해관계자, 요구사항, 수용 기준, 제약,
위험과 추적성을 소유한다. 아키텍처 구조, 선택의 근거, 구현 계약과 운영
절차는 소유하지 않는다. 실행 가능한 OpenAPI, GraphQL, Proto payload는
관련 Stage 03 Spec package가 소유한다.

## Contents

### Current Items

#### Package Index

| ID | 패키지 | 상태 |
| --- | --- | --- |
| REQ-0001 | [Gateway Tier (01-gateway) Requirements](0001-gateway.md) | `approved` |
| REQ-0002 | [02-Auth Requirements](0002-auth.md) | `approved` |
| REQ-0003 | [Security Tier (03-security) Requirements](0003-security.md) | `approved` |
| REQ-0004 | [Data Tier (04-data) Requirements](0004-data.md) | `approved` |
| REQ-0005 | [Analytics Services Requirements](0005-data-analytics.md) | `approved` |
| REQ-0006 | [Messaging Tier (05-messaging) Requirements](0006-messaging.md) | `approved` |
| REQ-0007 | [Observability Tier Requirements](0007-observability.md) | `approved` |
| REQ-0008 | [Workflow Tier (07-workflow) Requirements](0008-workflow.md) | `approved` |
| REQ-0009 | [AI Infrastructure Tier (08-ai) Requirements](0009-ai.md) | `approved` |
| REQ-0010 | [Platform Operations and Software Verification Requirements](0010-tooling.md) | `approved` |
| REQ-0011 | [Communication Tier (10-communication) Requirements](0011-communication.md) | `approved` |
| REQ-0012 | [Administration and Experimentation Requirements](0012-laboratory.md) | `approved` |
| REQ-0013 | [Open WebUI Requirements](0013-ai-open-webui.md) | `approved` |
| REQ-0023 | [Compose Network Segmentation Requirements](0023-standardize-infra-net.md) | `approved` |
| REQ-0024 | [Agent Governance Standardization Requirements](0024-agent-governance-standardization.md) | `approved` |
| REQ-0025 | [Operational Readiness Closure Requirements](0025-operational-readiness-closure.md) | `approved` |
| REQ-0026 | [Document Retention and Retirement Requirements](0026-document-retention-and-retirement.md) | `approved` |
| REQ-0027 | [Home and Development Host Requirements](0027-home-development-host.md) | `approved` |

```text
docs/01.requirements/
├── 0001-gateway.md
├── 0002-auth.md
├── ...
├── 0024-agent-governance-standardization.md
├── 0025-operational-readiness-closure.md
├── 0026-document-retention-and-retirement.md
├── 0027-home-development-host.md
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

파일명은 `####-<slug>.md`이고 frontmatter의 `type`은
`sdlc/requirement`, `artifact_id`는 `REQ-####`를 사용한다. 자식 ID는
반드시 `REQ-####-FR-####` 또는 `REQ-####-NFR-####` 전체 형태를 사용한다. 발급된 번호는 재사용하거나
high-water를 낮추지 않는다.

### Classification

#### PRD, SRS, and Interface Perspectives

Requirement Package 하나가 PRD의 문제·사용자 가치·범위, SRS의 functional·
non-functional 요구사항과 수용 기준, solution-independent interface 요구를
각 section 관점으로 함께 소유한다. Interface 요구는 `Functional Requirements`,
품질 요구는 `Quality Requirements` 절에 쓰며 별도 interface 절이나 `IF` 자식 ID는
발급하지 않는다. PRD, SRS, interface-requirement를 별도
profile이나 병렬 문서로 만들지 않는다. 실행 가능한 interface payload는
Stage 03 Spec의 contract가 소유한다.

## Workflow

### Create and Review

#### Authoring Flow

1. [`requirement-package.template.md`](../99.templates/templates/requirements/requirement-package.template.md)를 사용한다.
2. 동일한 문제와 범위를 소유하는 Requirement Package가 있는지 먼저 확인한다.
3. 패키지의 요구사항을 설명하는 Architecture Description과 중요한 선택을
   기록하는 ADR을 연결한다.
4. 구현 계약은 Stage 03 Spec, 운영 절차는 Stage 05에 둔다.
5. 변경 후 metadata와 repository-local link 검증을 실행한다.

#### Documentation Standards

- `type: sdlc/requirement`와 안정 ID를 사용한다. Registry profile `id`는
  template binding과 validator routing에만 사용하며 문서 frontmatter에 복제하지 않는다.
- `parent_ids`는 Requirement Package에서 선택 항목이며, 사용할 때는
  Registry가 요구하는 구조적 관계만 기록한다. 더 넓은 설계·명세·운영 연결은
  본문의 Traceability가 소유한다.
- 구현 방법이나 실행 순서를 요구사항으로 복사하지 않는다.
- 비어 있는 분류를 위해 별도 요구사항 문서를 만들지 않는다.
- 작성 의미와 역할 경계는 [공통 Agent 거버넌스 작성 정책](../../.agents/governance/documentation-protocol.md#role-specific-authoring)을 따른다.
- solution-independent interface 의미만 Stage 01에 두고 실행 가능한 계약은
  Stage 03에 둔다.

### Transition and Exit

Requirement Package는 draft → in-review → approved로 전이하며 approved에서 in-review로 돌아갈 수 있다. 삭제된 package의 번호는 Registry `reserved_history`가 보관하며, Stage 01 번호 공백은 그 번호가 예약된 경우에만 정당한다. 패키지를 추가·변경·삭제하면 같은 변경에서 이 README를 갱신한다.

## Related Documents

### Upstream and Downstream

- [Architecture](../02.architecture/README.md)
- [Architecture Descriptions](../02.architecture/descriptions/README.md)
- [Architecture Decisions](../02.architecture/decisions/README.md)
- [Specifications](../03.specs/README.md)
- [Operations](../05.operations/README.md)

### Policy and Templates

- [에이전트 작업 규칙](AGENTS.md)
- [문서 작성 계약](../../.agents/governance/documentation-protocol.md#readme-and-agentsmd): README와 AGENTS.md의 역할 구분
- [README 템플릿](../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다
