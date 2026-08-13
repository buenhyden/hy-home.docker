---
status: active
---

# Product Requirements

## Overview

`docs/01.requirements`는 제품의 문제, 이해관계자 가치, 범위, 요구사항과
수용 기준을 관리한다. 구현 구조는 Stage 02와 Stage 03, 실행 증거는 현재
변경 패킷, 운영 절차는 Stage 05가 소유한다.

## Audience

- Product Owners
- System Architects
- Developers
- AI Agents

## Scope

이 디렉터리는 현재 25개의 PRD를 보유한다. SRS와 Interface Requirement는
실제 역할이 필요한 경우에만 추가하며, 이 마이그레이션은 해당 문서를
만들지 않는다.

PRD는 문제와 이해관계자, 요구사항, 수용·검증 의도, 범위와 non-goal,
위험과 의존성을 소유한다. 아키텍처 구조, 선택의 근거, 구현 계약과 운영
절차는 소유하지 않는다.

## Structure

```text
docs/01.requirements/
├── prd-0001-gateway.md
├── prd-0002-auth.md
├── ...
├── prd-0024-agent-governance-standardization.md
├── prd-0025-operational-readiness-closure.md
└── README.md
```

파일명은 `prd-####-<slug>.md`이고 frontmatter의 `artifact_id`는
동일한 `prd-####`를 사용한다. 날짜는 경로가 아니라 `created`와 `updated`
metadata에 둔다.

## How to Work in This Area

1. [`prd.template.md`](../99.templates/templates/sdlc/prd.template.md)를 사용한다.
2. 동일한 문제와 범위를 소유하는 PRD가 있는지 먼저 확인한다.
3. PRD의 요구사항을 설명하는 Architecture Description과 중요한 선택을
   기록하는 ADR을 연결한다.
4. 구현 계약은 Stage 03 Spec, 운영 절차는 Stage 05에 둔다.
5. 변경 후 metadata와 repository-local link 검증을 실행한다.

## Documentation Standards

- `artifact_type: prd`와 안정 ID를 사용한다.
- PRD의 `parent_ids`는 비어 있다.
- 구현 방법이나 실행 순서를 요구사항으로 복사하지 않는다.
- 새 SRS 또는 Interface Requirement를 빈 분류 목적으로 만들지 않는다.

## AI Agent Guidance

Agent는 기존 PRD를 제자리에서 수정하고 병렬·호환 문서를 만들지 않는다.
연결된 Description, ADR, Spec 또는 Operations 문서가 실제로 존재할 때만
추적성 링크를 추가한다.

## Related Documents

- [Architecture](../02.architecture/README.md)
- [Architecture Descriptions](../02.architecture/descriptions/README.md)
- [Architecture Decisions](../02.architecture/decisions/README.md)
- [Specifications](../03.specs/README.md)
- [Operations](../05.operations/README.md)
- [Agent Governance Standardization PRD](./prd-0024-agent-governance-standardization.md)
- [Operational Readiness Closure PRD](./prd-0025-operational-readiness-closure.md)
