---
layer: agentic
---

# 99.templates

> stage 문서와 README 작성을 위한 공식 템플릿 원천

## Overview

이 폴더는 문서 템플릿을 저장합니다. 새 stage 문서와 folder README는 이 폴더의 대응 템플릿을 복사해 시작합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- `docs/01`부터 `docs/05`, `docs/90` stage 문서 템플릿
- `docs/00.agent-governance/memory/`의 memory note와 progress log 템플릿
- `docs/03.specs/<feature-id>/`에서 사용하는 보조 계약 템플릿
- repository-wide README 템플릿
- 템플릿과 stage folder 매핑

### Out of Scope

- 실제 요구사항, 설계, 계획, 작업, 운영, 사고 기록 본문
- 런타임 설정 원문이나 secret 값
- 템플릿을 벗어난 임의 문서 유형

## 템플릿 목록

- `agent-design.template.md`
- `data-model.template.md`
- `tests.template.md`
- `openapi.template.yaml`
- `service.template.proto`
- `schema.template.graphql`
- `prd.template.md`
- `ard.template.md`
- `adr.template.md`
- `spec.template.md`
- `api-spec.template.md`
- `plan.template.md`
- `task.template.md`
- `operation.template.md`
- `incident.template.md`
- `postmortem.template.md`
- `memory.template.md`
- `progress.template.md`
- `reference.template.md`
- `readme.template.md`

## 사용 원칙

1. 템플릿의 Target 경로를 실제 저장 위치와 맞춘다.
2. Placeholder는 모두 제거한다.
3. 상대 경로만 사용한다.
4. PRD/ARD/ADR/Spec/Plan/Task의 추적성을 유지한다.
5. Agent 기능은 Role, Tool, Guardrail, Eval, Fallback을 빠뜨리지 않는다.
6. `## Related Documents` 예시는 템플릿 파일 위치가 아니라 복사된 대상 파일 위치에서 해석되어야 하며, Markdown 템플릿에서는 가능한 경우 클릭 가능한 Markdown 링크 예시를 사용한다.
7. 운영 문서는 `operation.template.md`의 guide, policy, runbook profile 중 하나만 선택하고 나머지 profile 섹션을 제거한다.
8. infra service README는 목적, config, compose linkage, network, volume, port, label, secret ref, healthcheck, operations, validation, troubleshooting evidence를 포함한다.
9. scripts README는 `scripts/validation/`, `scripts/hardening/`, `scripts/hooks/`, `scripts/knowledge/`, `scripts/operations/`, `scripts/lib/` 목적 폴더를 보존하고 root-level wrapper를 만들지 않는다.
10. Markdown 템플릿의 cross-link 예시는 복사된 Target 위치 기준으로 계산하고, YAML/GraphQL/Proto 계약 파일의 cross-link는 parent Markdown Spec 또는 API Spec에서 관리한다.

## 템플릿-폴더 매핑

| Folder                                   | Template                 |
| ---------------------------------------- | ------------------------ |
| `01.requirements/`                       | `prd.template.md`        |
| `02.architecture/requirements/`          | `ard.template.md`        |
| `02.architecture/decisions/`             | `adr.template.md`        |
| `03.specs/`                              | `spec.template.md`       |
| `03.specs/<feature-id>/api-spec.md`      | `api-spec.template.md`   |
| `04.execution/plans/`                    | `plan.template.md`       |
| `04.execution/tasks/`                    | `task.template.md`       |
| `05.operations/guides/`                  | `operation.template.md`  |
| `05.operations/policies/`                | `operation.template.md`  |
| `05.operations/runbooks/`                | `operation.template.md`  |
| `05.operations/incidents/`               | `incident.template.md`   |
| `05.operations/incidents/`               | `postmortem.template.md` |
| `00.agent-governance/memory/<note>.md`   | `memory.template.md`     |
| `00.agent-governance/memory/progress.md` | `progress.template.md`   |
| `90.references/`                         | `reference.template.md`  |
| `README.md` (per folder)                 | `readme.template.md`     |

## API Spec 템플릿 위치

API 계약 문서는 별도 유형이 아니라 `03.specs/` 아래에서 사용하는 하위 템플릿이다.

- 올바른 위치: `docs/03.specs/<feature-id>/api-spec.md`
- 잘못된 패턴: `docs/api/...`

## README 템플릿

각 폴더 README도 반복적으로 재사용되는 문서 유형이므로 별도 README 템플릿을 함께 제공한다.

## Structure

```text
99.templates/
├── *.template.md       # Markdown stage and README templates
├── *.template.yaml     # OpenAPI contract template
├── *.template.graphql  # GraphQL schema template
├── *.template.proto    # Protobuf service contract template
└── README.md           # This file
```

## How to Work in This Area

1. 새 문서를 만들기 전에 [`../00.agent-governance/rules/stage-authoring-matrix.md`](../00.agent-governance/rules/stage-authoring-matrix.md)의 대상 stage row를 확인한다.
2. 대응 템플릿을 복사한 뒤 placeholder를 모두 실제 값으로 교체한다.
3. README는 [`readme.template.md`](./readme.template.md)의 base structure와 경로별 snippet을 조합한다.
4. 템플릿 자체를 바꿀 때는 [`../00.agent-governance/rules/documentation-protocol.md`](../00.agent-governance/rules/documentation-protocol.md)의 DOCS 3 RULES와 repository contract 검증을 함께 확인한다.

## Spec 하위 보조 문서 템플릿

`03.specs/<feature-id>/` 아래에서 반복적으로 사용하는 보조 설계 문서와 계약 파일용 템플릿을 함께 제공한다.

## 예시

- 새 운영 문서: `operation.template.md`를 복사해 `docs/05.operations/<guides|policies|runbooks>/<topic>.md` 또는 `docs/05.operations/<guides|policies|runbooks>/<domain>/<topic>.md`로 작성한다.
- 운영 문서는 `guides/`가 사용 맥락, `policies/`가 통제/예외/검토 기준, `runbooks/`가 순서 있는 절차와 evidence를 담당한다.
- 운영 문서 cross-link는 복사된 Target 기준으로 계산한다. 예: `docs/05.operations/guides/<topic>.md`에서는 `../../02.architecture/...`, `docs/05.operations/guides/<domain>/<topic>.md`에서는 `../../../02.architecture/...`, `docs/05.operations/guides/<domain>/<subdomain>/<topic>.md`에서는 `../../../../02.architecture/...`를 사용한다.
- 새 사고 기록: `incident.template.md`를 복사해 `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`로 작성한다.
- 새 사후 분석: `postmortem.template.md`를 복사해 `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md`로 작성한다.
- 새 governance memory note: `memory.template.md`를 복사해 `docs/00.agent-governance/memory/<short-title>.md`로 작성한다.
- agent progress log 변경: `progress.template.md`를 기준으로 `docs/00.agent-governance/memory/progress.md`를 갱신한다.
- 새 참고 문서: `reference.template.md`를 복사해 `docs/90.references/<category>/<item>.md`로 작성한다.

## Related Documents

- [docs index](../README.md)
- [Documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
