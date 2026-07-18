---
layer: agentic
---

# Template Artifacts

## Overview

`docs/99.templates/templates`는 단계 문서와 재사용 가능한 계약을 위한
복사 가능한 원본 템플릿을 제공한다. 선택, 수명주기, 변경 거버넌스는
[support](../support/README.md)에서 관리한다.

## Audience

- Documentation Writers
- AI Agents
- Repository Maintainers
- QA Engineers

## Scope

- Markdown 문서 형식과 기계 판독 가능한 계약 형식을 분류한다.
- 템플릿 원본의 canonical 경로를 안내한다.
- 공유 규칙과 검증 의미는 Stage 99 support 문서로 연결한다.

## Structure

| Category | Path | Templates |
| --- | --- | --- |
| SDLC | [sdlc/](./sdlc/README.md) | `prd`, `ard`, `adr`, `spec`, `plan`, `task` |
| Spec contracts | [spec-contracts/](./spec-contracts/README.md) | `api-spec`, `agent-design`, `data-model`, `service`, `tests`, `openapi`, `schema`, `proto` |
| Operations | [operations/](./operations/README.md) | `guide`, `policy`, `runbook`, `incident`, `postmortem`, `release` |
| Governance | [governance/](./governance/README.md) | `memory`, `progress` |
| Common | [common/](./common/README.md) | `readme`, `reference`, `audit`, `archive`, `content-archive` |

## How to Work in This Area

1. [template selection](../support/template-selection.md)에서 목적과 대상 경로에 맞는 원본을 찾는다.
2. Markdown 형식은 해당 원본을 복사하고 모든 토큰을 실제 내용으로 바꾼다.
3. 기계 판독 형식은 부모 Markdown 문서의 교차 링크 소유권을 유지한다.
4. 변경 후 [template contract](../support/template-contract.md)와 저장소 검증을 확인한다.

## Related Documents

- [template catalog](../README.md)
- [support README](../support/README.md)
- [template contract](../support/template-contract.md)
- [template selection](../support/template-selection.md)
