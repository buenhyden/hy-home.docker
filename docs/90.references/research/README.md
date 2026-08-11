---
status: active
---
<!-- Target: docs/90.references/research/README.md -->

# Research References

> 외부 source-backed 조사와 repo-local 분석을 함께 보관하는 reference category

## Overview

`docs/90.references/research`는 active stage 문서를 보조하는 조사형 reference를 관리합니다. 이 폴더의 문서는 외부 표준, 공식 제품 문서, 논문, 공식 repository, repo-local canonical 파일을 함께 읽고 느리게 변하는 분석 기준을 제공합니다.

이 category는 정책, 실행 계획, 운영 runbook, task evidence를 대체하지 않습니다. 현재 정책은 `docs/00.agent-governance/`와 `docs/05.operations/policies/`, 실행 계획과 evidence는 `docs/04.execution/`, runtime truth는 `infra/`, `scripts/`, provider runtime surface가 담당합니다.

## Category Role

`docs/90.references/research`는 source-backed research pack을 위한 reference category입니다. 외부 자료와 repo-local evidence를 함께 분석하지만, active stage의 승인된 요구사항, 결정, 계획, 운영 절차, runtime 설정 원문을 대신하지 않습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 외부 공식 문서와 repo-local evidence를 함께 분석한 reference pack
- 하네스 엔지니어링, 루프 엔지니어링, SDLC, QA, CI/CD, formatting, 문서 architecture, LLM Wiki, memory hierarchy 같은 cross-cutting research
- active stage 문서가 반복해서 참조할 수 있는 source-backed facts
- 다른 stage에서 후속 보완이 필요한 gap 기록

### Out of Scope

- active policy 본문
- implementation plan 또는 task evidence
- 운영 runbook 절차
- 최신 runtime 설정 원문
- secret 값, credential, token, private key, shell history, raw log

## Structure

```text
research/
├── README.md # This file
├── 2026-08-08-agentic-engineering-research-pack/ # Canonical human route for the rebuilt 20-leaf / 21-file pack
└── 2026-07-05-agentic-research-pack-refresh/ # Superseded historical pack; deletion remains gated
```

## Current References

- [2026-08-08-agentic-engineering-research-pack/README.md](./2026-08-08-agentic-engineering-research-pack/README.md) - agentic engineering의 canonical human research route입니다. 20개 leaf, 21개 file, evidence class, reading route, 14-scope route, canonical-owner boundary, migration state를 이 index에서 읽습니다.

## Superseded Paths

`docs/90.references/research/2026-07-05-agentic-research-pack-refresh/`는
Task 9에서 superseded 되었지만 삭제하거나 수정하지 않았습니다. repository-wide
cross-link와 generated route 전환은 Task 10, old-pack 삭제 gate는 Task 11이
소유합니다. `2026-07-07-agentic-research-pack-update/`는 이전 Spec 122에서 이미
제거된 redirect-only path입니다. 아래 표가 두 predecessor의 human destination
mapping을 제공합니다.

| 제거된 경로 | Canonical destination |
| --- | --- |
| `2026-07-05-agentic-research-pack-refresh/` | [canonical 2026-08-08 pack index](./2026-08-08-agentic-engineering-research-pack/README.md) |
| `2026-07-07-agentic-research-pack-update/README.md` | [canonical pack index](./2026-08-08-agentic-engineering-research-pack/README.md) |
| `2026-07-07-agentic-research-pack-update/workspace-baseline.md` | [workspace baseline](./2026-08-08-agentic-engineering-research-pack/workspace-baseline.md), [spec-driven SDLC](./2026-08-08-agentic-engineering-research-pack/spec-driven-sdlc.md), [document roles](./2026-08-08-agentic-engineering-research-pack/sdlc-document-roles.md), [quality](./2026-08-08-agentic-engineering-research-pack/quality-ci-formatting.md), [automation](./2026-08-08-agentic-engineering-research-pack/automation-pipeline-workflow.md), [Compose](./2026-08-08-agentic-engineering-research-pack/docker-compose-infrastructure.md), [security](./2026-08-08-agentic-engineering-research-pack/security-governance.md) |
| `2026-07-07-agentic-research-pack-update/harness-engineering.md` | [harness engineering](./2026-08-08-agentic-engineering-research-pack/harness-engineering.md), [provider implementation](./2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md) |
| `2026-07-07-agentic-research-pack-update/loop-engineering.md` | [loop engineering](./2026-08-08-agentic-engineering-research-pack/loop-engineering.md), [automation](./2026-08-08-agentic-engineering-research-pack/automation-pipeline-workflow.md), [quality](./2026-08-08-agentic-engineering-research-pack/quality-ci-formatting.md) |
| `2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md` | [provider implementation](./2026-08-08-agentic-engineering-research-pack/provider-implementation-comparison.md), [provider model landscape](./2026-08-08-agentic-engineering-research-pack/provider-model-landscape.md), [agent model selection](./2026-08-08-agentic-engineering-research-pack/agent-model-selection.md) |
| `2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md` | [AI agent catalogs](./2026-08-08-agentic-engineering-research-pack/ai-agent-catalogs.md) |

제거 근거와 이력은 [Spec 122](../../98.archive/03.specs/122-agentic-research-pack-consolidation/spec.md), [통합 Plan](../../04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md), [통합 Task](../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md), [확장 Task](../../04.execution/tasks/2026-08-07-agentic-research-pack-extension.md)에 남아 있습니다.

## Naming Rules

- SDLC-linked research packs live under `<date>-<sdlc_key>/`.
- Pack-level report files use descriptive names such as `workspace-baseline.md` or `quality-ci-formatting.md`.
- Do not use `part-*.md` prefixes for finalized report files.

## How to Work in This Area

1. 새 research 문서가 active decision, policy, plan, runbook을 대체하지 않는지 확인합니다.
2. agentic engineering의 current research route는 2026-08-08 canonical pack에서 읽습니다. 2026-07-05와 제거된 2026-07-07 경로는 위 Superseded Paths 표로 라우팅합니다.
3. 새 non-README reference는 [reference.template.md](../../99.templates/templates/common/reference.template.md)의 필수 섹션을 따릅니다.
4. 새 non-README reference는 closed-surface contract에 맞춰 영어로 작성합니다.
5. 외부 자료는 공식 vendor docs, 표준 기관 문서, 원 논문, 공식 repository를 우선합니다.
6. source가 빠르게 변하는 제품 문서이면 문서 안에 재검증 필요성을 명시합니다.
7. 새 category나 pack을 추가하면 이 README와 [90.references](../README.md)를 함께 갱신합니다.
8. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [90.references](../README.md)
- [docs index](../../README.md)
- [reference template](../../99.templates/templates/common/reference.template.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
