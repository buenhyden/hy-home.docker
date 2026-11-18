---
title: "Architecture Descriptions"
version: "1.4.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "architecture"
---

# Architecture Descriptions

## Responsibility

### Purpose

#### Purpose and Readers

`docs/02.architecture/descriptions`는 시스템 또는 관심사별 현재 아키텍처를
설명한다. 각 문서는 이해관계자와 경계, 구성 요소, runtime과 배포 view,
품질 속성·위험·발전 방향, 관련 Requirement·ADR·Spec·Operations 문서를
기록한다.

#### Audience

- System Architects
- Developers
- Operators

#### Inputs and Outputs

이 디렉터리는 현재 유효한 Description을 보유한다. Description은 구현
계획이나 운영 절차를 소유하지 않고 실제로 연결된 Requirement Package, ADR, Spec과
Operations 문서의 역할을 대체하지 않는다. 개수는 유지 기준이 아니므로 아래
Current Inventory와 실제 파일 목록이 권위이다.

### Excluded Responsibilities

Description은 구현 계획이나 운영 절차를 소유하지 않고, 실제로 연결된 Requirement Package, ADR, Spec과 Operations 문서의 역할을 대체하지 않는다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [0001-gateway-architecture.md](./0001-gateway-architecture.md) | Gateway Tier Architecture Description |
| [0002-auth-architecture.md](./0002-auth-architecture.md) | 02-Auth Architecture Description |
| [0003-security-architecture.md](./0003-security-architecture.md) | Security Tier Architecture Description |
| [0004-data-architecture.md](./0004-data-architecture.md) | Data Tier (04-data) Architecture Description |
| [0005-messaging-architecture.md](./0005-messaging-architecture.md) | Messaging Architecture Description |
| [0006-observability-architecture.md](./0006-observability-architecture.md) | Observability Architecture Description |
| [0007-workflow-architecture.md](./0007-workflow-architecture.md) | Workflow Tier (07-workflow) Architecture Description |
| [0008-ai-architecture.md](./0008-ai-architecture.md) | AI Infrastructure Architecture Description |
| [0009-tooling-architecture.md](./0009-tooling-architecture.md) | Platform Operations and Software Verification Architecture Description |
| [0010-communication-architecture.md](./0010-communication-architecture.md) | Communication Tier Architecture Description |
| [0011-laboratory-architecture.md](./0011-laboratory-architecture.md) | Administration and Experimentation Architecture Description |
| [0012-data-analytics-architecture.md](./0012-data-analytics-architecture.md) | Analytics Tier Architecture Description |
| [0013-open-webui-architecture.md](./0013-open-webui-architecture.md) | Open WebUI Architecture Description |
| [0018-security-optimization-hardening-architecture.md](./0018-security-optimization-hardening-architecture.md) | Security Optimization and Hardening Architecture |
| [0019-data-optimization-hardening-architecture.md](./0019-data-optimization-hardening-architecture.md) | Data Optimization and Hardening Architecture |
| [0020-messaging-optimization-hardening-architecture.md](./0020-messaging-optimization-hardening-architecture.md) | 05-Messaging Optimization Hardening Architecture Description |
| [0021-observability-optimization-hardening-architecture.md](./0021-observability-optimization-hardening-architecture.md) | 06-Observability Optimization Hardening Architecture Description |
| [0022-workflow-optimization-hardening-architecture.md](./0022-workflow-optimization-hardening-architecture.md) | 07-Workflow Optimization Hardening Architecture Description |
| [0023-ai-optimization-hardening-architecture.md](./0023-ai-optimization-hardening-architecture.md) | 08-AI Optimization Hardening Architecture Description |
| [0024-tooling-optimization-hardening-architecture.md](./0024-tooling-optimization-hardening-architecture.md) | Platform Operations and Quality Optimization Hardening Architecture Description |
| [0025-laboratory-optimization-hardening-architecture.md](./0025-laboratory-optimization-hardening-architecture.md) | Admin and Experiment Tools Hardening Architecture Description |
| [0026-standardize-infra-net.md](./0026-standardize-infra-net.md) | Compose Network Segmentation Architecture Description |
| [0027-agent-governance-canonical-adapter.md](./0027-agent-governance-canonical-adapter.md) | Agent Governance Canonical Adapter Architecture |
| [0028-operational-readiness-closure.md](./0028-operational-readiness-closure.md) | Operational Readiness Closure Architecture |
| [0030-document-lifecycle-governance.md](./0030-document-lifecycle-governance.md) | Document Lifecycle Governance Architecture |
| [0031-home-development-host.md](./0031-home-development-host.md) | Home and Development Host Architecture |
| [0032-experience-architecture.md](./0032-experience-architecture.md) | Experience Tier Architecture Description |

#### Current Items

```text
docs/02.architecture/descriptions/
├── 0001-gateway-architecture.md
├── 0002-auth-architecture.md
├── ...
├── 0027-agent-governance-canonical-adapter.md
├── 0028-operational-readiness-closure.md
├── 0030-document-lifecycle-governance.md
├── 0031-home-development-host.md
├── 0032-experience-architecture.md
└── README.md
```

#### Current Inventory

`AD-0001`부터 `AD-0013`은 기본 tier와 서비스, `AD-0018`부터 `AD-0025`는
각 tier의 hardening, `AD-0026` 이후는 network와 cross-cutting 아키텍처이다.

| ID | 제목 | 상태 |
| --- | --- | --- |
| [`AD-0001`](./0001-gateway-architecture.md) | Gateway Tier Architecture Description | `approved` |
| [`AD-0002`](./0002-auth-architecture.md) | 02-Auth Architecture Description | `approved` |
| [`AD-0003`](./0003-security-architecture.md) | Security Tier Architecture Description | `approved` |
| [`AD-0004`](./0004-data-architecture.md) | Data Tier (04-data) Architecture Description | `approved` |
| [`AD-0005`](./0005-messaging-architecture.md) | Messaging Architecture Description | `approved` |
| [`AD-0006`](./0006-observability-architecture.md) | Observability Architecture Description | `approved` |
| [`AD-0007`](./0007-workflow-architecture.md) | Workflow Tier (07-workflow) Architecture Description | `approved` |
| [`AD-0008`](./0008-ai-architecture.md) | AI Infrastructure Architecture Description | `approved` |
| [`AD-0009`](./0009-tooling-architecture.md) | Platform Operations and Software Verification Architecture Description | `approved` |
| [`AD-0010`](./0010-communication-architecture.md) | Communication Tier Architecture Description | `approved` |
| [`AD-0011`](./0011-laboratory-architecture.md) | Administration and Experimentation Architecture Description | `approved` |
| [`AD-0012`](./0012-data-analytics-architecture.md) | Analytics Tier Architecture Description | `approved` |
| [`AD-0013`](./0013-open-webui-architecture.md) | Open WebUI Architecture Description | `approved` |
| [`AD-0018`](./0018-security-optimization-hardening-architecture.md) | Security Optimization and Hardening Architecture | `approved` |
| [`AD-0019`](./0019-data-optimization-hardening-architecture.md) | Data Optimization and Hardening Architecture | `approved` |
| [`AD-0020`](./0020-messaging-optimization-hardening-architecture.md) | 05-Messaging Optimization Hardening Architecture Description | `approved` |
| [`AD-0021`](./0021-observability-optimization-hardening-architecture.md) | 06-Observability Optimization Hardening Architecture Description | `approved` |
| [`AD-0022`](./0022-workflow-optimization-hardening-architecture.md) | 07-Workflow Optimization Hardening Architecture Description | `approved` |
| [`AD-0023`](./0023-ai-optimization-hardening-architecture.md) | 08-AI Optimization Hardening Architecture Description | `approved` |
| [`AD-0024`](./0024-tooling-optimization-hardening-architecture.md) | Platform Operations and Quality Optimization Hardening Architecture Description | `approved` |
| [`AD-0025`](./0025-laboratory-optimization-hardening-architecture.md) | Admin and Experiment Tools Hardening Architecture Description | `approved` |
| [`AD-0026`](./0026-standardize-infra-net.md) | Compose Network Segmentation Architecture Description | `approved` |
| [`AD-0027`](./0027-agent-governance-canonical-adapter.md) | Agent Governance Canonical Adapter Architecture | `approved` |
| [`AD-0028`](./0028-operational-readiness-closure.md) | Operational Readiness Closure Architecture | `approved` |
| [`AD-0030`](./0030-document-lifecycle-governance.md) | Document Lifecycle Governance Architecture | `approved` |
| [`AD-0031`](./0031-home-development-host.md) | Home and Development Host Architecture | `approved` |
| [`AD-0032`](./0032-experience-architecture.md) | Experience Tier Architecture Description | `approved` |

#### C4 and arc42 Placement

C4와 arc42의 비례적 적용 원칙과 diagram 품질 기준은
[공통 Agent 거버넌스 작성 정책](../../00.workspace/02.process/documentation-protocol.md#role-specific-authoring)이
소유한다. 템플릿의 `Context and Boundaries`, `Structure`의 `Building Blocks`와
`Interfaces`, `Runtime Behavior`의 `Normal Flow`와 `Failure and Recovery`,
`Quality Scenarios`의 `Scenarios`와 `Trade-offs`에 해당 내용을 배치한다.
빈 framework section이나 병렬 문서를 만들지 않으며 선택·대안·근거는 ADR이
소유한다.

### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`이다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않는다.

## Usage

### Entry Points

#### Upstream and Downstream

- [Architecture](../README.md)
- [Product Requirements](../../01.requirements/README.md)
- [Architecture Decisions](../decisions/README.md)
- [Specifications](../../03.specs/README.md)
- [Operations](../../05.operations/README.md)

#### Policy and Templates

- [에이전트 작업 규칙](../AGENTS.md)
- [Architecture Description Template](../../99.templates/templates/architecture/description.template.md)
- [문서 작성 계약](../../00.workspace/02.process/documentation-protocol.md#readme-and-agentsmd): README와 AGENTS.md의 역할 구분
- [README 템플릿](../../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

### Checks

#### Authoring Flow

1. 상위 [Requirement Package](../../01.requirements/README.md)를 확인한다.
2. 같은 system, tier 또는 concern을 설명하는 문서가 있는지 확인한다.
3. 새 문서는
   [`description.template.md`](../../99.templates/templates/architecture/description.template.md)를 사용한다.
4. 현재 구현과 저장소 사실만 설명하고 확인되지 않은 runtime 구조를 만들지
   않는다.
5. material choice는 [ADR](../decisions/README.md)에 기록한다.

#### Documentation Standards

- `<4-digit-id>-<slug>.md`, `artifact_id: AD-<4-digit-id>`,
  `type: sdlc/architecture-description`을 일치시킨다.
- `parent_ids`는 실제 상위 Requirement Package의 `REQ-####` ID만 포함한다.
- 관련 결정과 구현 명세가 존재하면 typed link로 연결한다.
- Description은 selection rationale나 실행 절차를 복제하지 않는다.

#### Transition and Exit

Architecture Description은 draft → in-review → approved로 전이하며 approved에서 in-review로 돌아갈 수 있다. 더 이상 현재 구조를 설명하지 않는 문서는 내용을 현재 소유자에 요약하고 삭제하며 번호를 Registry `reserved_history`에 추가한다.
