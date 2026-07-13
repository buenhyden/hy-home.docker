---
layer: agentic
---

# 99.templates

> stage 문서와 README 작성을 위한 canonical template entrypoint

## Overview

`docs/99.templates`는 워크스페이스 문서 템플릿의 canonical source입니다.
복사 가능한 템플릿은 `templates/`에 두고, 템플릿을 어떻게 선택하고 관리할지에
대한 contract와 governance는 `support/`에 둡니다.

이 README는 catalog와 routing entrypoint만 담당합니다. 상세 lifecycle,
frontmatter, cross-link, stale document, deviation, README profile 규칙은
support 문서를 기준으로 확인합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- `docs/01`부터 `docs/05`, `docs/90`, `docs/98` stage 문서 템플릿
- `docs/00.agent-governance/memory/`의 memory note와 progress log 템플릿
- `docs/03.specs/NNN-<feature-id>/`에서 사용하는 child contract 템플릿
- repository-wide README와 folder README 템플릿
- template contract, frontmatter contract, lifecycle/status, selection guide

### Out of Scope

- 실제 요구사항, 설계, 계획, 작업, 운영, 사고 기록 본문
- 런타임 설정 원문이나 secret 값
- 템플릿을 벗어난 임의 문서 유형
- Stage 00 governance rule 본문을 대체하는 별도 정책 원천

## Category Catalog

| Category | Path | Role |
| --- | --- | --- |
| SDLC templates | [templates/sdlc/](./templates/sdlc/) | PRD, ARD, ADR, Spec, Plan, Task |
| Spec contract templates | [templates/spec-contracts/](./templates/spec-contracts/) | API spec, agent design, data model, service, tests, OpenAPI, GraphQL, Proto |
| Operations templates | [templates/operations/](./templates/operations/) | Guide, policy, runbook, incident, postmortem, Release |
| Governance templates | [templates/governance/](./templates/governance/) | Memory note, progress log |
| Common templates | [templates/common/](./templates/common/) | README, reference, archive |
| Support governance | [support/](./support/) | Template contract, governance, frontmatter, lifecycle, selection, external-source rationale |

## Structure

```text
99.templates/
├── README.md        # This file
├── support/         # Non-copyable template rules and governance
└── templates/       # Copyable template artifacts
```

## How to Work in This Area

이 섹션은 Stage 99 작업 경로를 찾기 위한 routing map입니다.

- Template 선택: [template selection guide](./support/template-selection.md)
- 복사 가능한 template catalog: [templates README](./templates/README.md)
- 실제 release event 기록: [Release template](./templates/operations/release.template.md)
- Frontmatter와 lifecycle status: [frontmatter contract](./support/frontmatter-contract.md), [lifecycle status](./support/lifecycle-status.md)
- Template 변경과 검토: [template governance](./support/template-governance.md)
- Durable support rule surface: [support README](./support/README.md)

## Related Documents

- [templates README](./templates/README.md)
- [support README](./support/README.md)
- [template contract](./support/template-contract.md)
- [template governance](./support/template-governance.md)
- [frontmatter contract](./support/frontmatter-contract.md)
- [template selection guide](./support/template-selection.md)
- [docs index](../README.md)
- [Documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
