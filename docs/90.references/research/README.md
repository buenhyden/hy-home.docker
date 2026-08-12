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
├── ref-0039-readme.md # Canonical agentic engineering research index
├── ref-<id>-<slug>.md # Stable source-backed research artifact
└── README.md # This file
```

## Current References

- [ref-0039-readme.md](ref-0039-readme.md) - 현재 agentic engineering의 유일한 active canonical research pack입니다. current facts와 source-backed comparison은 이 pack에서 읽어야 합니다.

## Superseded Paths

`docs/90.references/research/2026-07-07-agentic-research-pack-update/`는 제거되었습니다. 이 pack은 Spec 122에서 canonical pack으로 통합된 뒤 redirect stub만 남아 있었고, 분석 본문을 보유하지 않았습니다. 아래 표가 그 경로의 canonical destination mapping을 대신합니다.

| 제거된 경로 | Canonical destination |
| --- | --- |
| `2026-07-07-agentic-research-pack-update/README.md` | [canonical pack index](ref-0039-readme.md) |
| `2026-07-07-agentic-research-pack-update/workspace-baseline.md` | [workspace baseline](ref-0058-workspace-baseline.md), [spec-driven SDLC](ref-0057-spec-driven-sdlc.md), [document roles](ref-0055-sdlc-document-roles.md), [quality](ref-0053-quality-ci-formatting.md), [automation](ref-0043-automation-pipeline-workflow.md), [Compose](ref-0044-docker-compose-infrastructure.md), [security](ref-0056-security-governance.md) |
| `2026-07-07-agentic-research-pack-update/harness-engineering.md` | [harness engineering](ref-0047-harness-engineering.md), [provider implementation](ref-0051-provider-implementation-comparison.md) |
| `2026-07-07-agentic-research-pack-update/loop-engineering.md` | [loop engineering](ref-0049-loop-engineering.md), [automation](ref-0043-automation-pipeline-workflow.md), [quality](ref-0053-quality-ci-formatting.md) |
| `2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md` | [provider implementation](ref-0051-provider-implementation-comparison.md), [provider model landscape](ref-0052-provider-model-landscape.md), [agent model selection](ref-0041-agent-model-selection.md) |
| `2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md` | [AI agent catalogs](ref-0042-ai-agent-catalogs.md) |

제거 근거와 이력은 Spec 122, 통합 Plan, 통합 Task, [확장 Task](../../03.specs/spec-0123-agentic-engineering-audit-remediation/task.md)에 남아 있습니다.

## Naming Rules

- Research artifacts use `ref-<id>-<slug>.md`; a pack index uses `ref-<id>-readme.md`.
- Store the observation date in `observed_at`, not in the path. Preserve body timeline dates as historical evidence.
- Do not use `part-*.md` prefixes for finalized report files.

## How to Work in This Area

1. 새 research 문서가 active decision, policy, plan, runbook을 대체하지 않는지 확인합니다.
2. agentic engineering의 current facts는 [ref-0039](ref-0039-readme.md)에서만 읽습니다. 제거된 경로는 위 Superseded Paths 표의 historical provenance로만 해석합니다.
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
