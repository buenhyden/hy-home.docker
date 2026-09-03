---
title: Requirement Packages
version: 1.0.0
type: common/readme
layer: requirements
status: active
owner: "@buenhyden"
---

# Requirement Packages

## Overview

`docs/01.requirements`는 제품의 문제, 이해관계자 가치, 범위, 요구사항과
수용 기준을 하나의 Requirement Package로 관리한다. 구현 구조는 Stage 02와
Stage 03, 실행 증거는 현재 변경 패킷, 운영 절차는 Stage 05가 소유한다.

## Audience

- Product Owners
- System Architects
- Developers
- AI Agents

## Scope

이 디렉터리는 현재 25개의 Requirement Package를 보유한다. 각 패키지는
functional, non-functional, solution-independent interface 요구사항을 같은
경계에서 관리한다. 별도 역할 문서를 병렬로 만들지 않는다.

Requirement Package는 문제와 이해관계자, 요구사항, 수용 기준, 제약,
위험과 추적성을 소유한다. 아키텍처 구조, 선택의 근거, 구현 계약과 운영
절차는 소유하지 않는다. 실행 가능한 OpenAPI, GraphQL, Proto payload는
관련 Stage 03 Spec package가 소유한다.

## Structure

```text
docs/01.requirements/
├── 0001-gateway.md
├── 0002-auth.md
├── ...
├── 0024-agent-governance-standardization.md
├── 0025-operational-readiness-closure.md
├── 0026-document-retention-and-retirement.md
└── README.md
```

파일명은 `####-<slug>.md`이고 frontmatter의 `profile_id`와 `artifact_type`은
`requirements-package`, `artifact_id`는 `REQ-####`를 사용한다. 자식 ID는
반드시 `REQ-####-FR-####`, `REQ-####-NFR-####`, 또는
`REQ-####-IF-####` 전체 형태를 사용한다. 발급된 번호는 재사용하거나
high-water를 낮추지 않는다.

## How to Work in This Area

1. [`requirement-package.template.md`](../99.templates/templates/requirements/requirement-package.template.md)를 사용한다.
2. 동일한 문제와 범위를 소유하는 Requirement Package가 있는지 먼저 확인한다.
3. 패키지의 요구사항을 설명하는 Architecture Description과 중요한 선택을
   기록하는 ADR을 연결한다.
4. 구현 계약은 Stage 03 Spec, 운영 절차는 Stage 05에 둔다.
5. 변경 후 metadata와 repository-local link 검증을 실행한다.

### Documentation Standards

- `profile_id: requirements-package`, `artifact_type: requirements-package`와
  안정 ID를 사용한다.
- Requirement Package의 `parent_ids`는 비어 있다.
- 구현 방법이나 실행 순서를 요구사항으로 복사하지 않는다.
- 비어 있는 분류를 위해 별도 요구사항 문서를 만들지 않는다.
- solution-independent interface 의미만 Stage 01에 두고 실행 가능한 계약은
  Stage 03에 둔다.

### AI Agent Guidance

Agent는 기존 Requirement Package를 제자리에서 수정하고 병렬·호환 문서를
만들지 않는다.
연결된 Description, ADR, Spec 또는 Operations 문서가 실제로 존재할 때만
추적성 링크를 추가한다.

## Related Documents

- [Architecture](../02.architecture/README.md)
- [Architecture Descriptions](../02.architecture/descriptions/README.md)
- [Architecture Decisions](../02.architecture/decisions/README.md)
- [Specifications](../03.specs/README.md)
- [Operations](../05.operations/README.md)
- [Agent Governance Standardization Requirements](./0024-agent-governance-standardization.md)
- [Operational Readiness Closure Requirements](./0025-operational-readiness-closure.md)
- [문서 보존 및 은퇴 요구사항](./0026-document-retention-and-retirement.md)
