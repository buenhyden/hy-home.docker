# docs

> Shared harness-engineering and agent-first engineering documentation space for staged repository knowledge.

## Overview

`docs/`는 shared harness-engineering and agent-first engineering 목적에 맞춰 프로젝트의 요구사항, 아키텍처, 결정 사항, 기술 명세, 실행 증거, 운영 지식을 통합 관리하는 표준 공간입니다. 활성 문서는 허용된 taxonomy 안에서만 관리하며, 검증 스크립트가 이 계약을 강제합니다.

현재 문서 흐름은 `01.requirements -> 02.architecture -> 03.specs -> 04.execution -> 05.operations`입니다. 보조 공간으로 `00.agent-governance`, `90.references`, `98.archive`, `99.templates`를 사용합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 공식 stage 문서 taxonomy와 작성 원칙
- 문서 유형별 템플릿 매핑
- 문서 추적성, 검증, README 작성 기준
- Agent governance와 사람 대상 문서의 경계

### Out of Scope

- Docker Compose runtime 설정 원문
- secret 값, credential, token, 인증서 원문
- 임시 scratch 문서나 비표준 active stage 폴더
- 개별 서비스의 상세 운영 절차 본문

## Structure

```text
docs/
├── 00.agent-governance/        # AI Agent 실행 정책, provider 계약, scope, rule, runtime catalog
├── 01.requirements/            # 제품/시스템 요구사항
├── 02.architecture/            # 아키텍처 요구사항과 결정 기록
│   ├── requirements/
│   └── decisions/
├── 03.specs/                   # 컴포넌트/기능별 상세 설계 명세
├── 04.execution/               # 실행 계획과 작업 증거
│   ├── plans/
│   └── tasks/
├── 05.operations/              # 운영 가이드, 정책, 런북, 사고 기록
│   ├── guides/
│   ├── policies/
│   ├── runbooks/
│   └── incidents/
├── 90.references/              # 느리게 변하는 참고 지식, 표준, 학습 로드맵, LLM Wiki
├── 98.archive/                 # active chain에서 제거된 old 문서 tombstone
├── 99.templates/               # stage 문서 작성을 위한 표준 템플릿
└── README.md                   # This file
```

## Routing

| I need to... | Go to |
| --- | --- |
| define user value or requirements | `01.requirements/` |
| describe architecture requirements | `02.architecture/requirements/` |
| record an architecture decision | `02.architecture/decisions/` |
| write a technical specification | `03.specs/` |
| plan implementation work | `04.execution/plans/` |
| record task evidence | `04.execution/tasks/` |
| operate or configure a service | `05.operations/guides/` |
| define operational controls | `05.operations/policies/` |
| execute recovery or repeatable procedures | `05.operations/runbooks/` |
| record incidents or postmortems | `05.operations/incidents/` |
| provide LLM-facing repository navigation | `90.references/llm-wiki/` |
| trace removed old documents | `98.archive/` |

## Migration Map

이전 stage 이름은 다음 canonical 경로로 이관되었습니다.

| Old Path | New Path |
| --- | --- |
| `docs/01.prd/` | `docs/01.requirements/` |
| `docs/02.ard/` | `docs/02.architecture/requirements/` |
| `docs/03.adr/` | `docs/02.architecture/decisions/` |
| `docs/04.specs/` | `docs/03.specs/` |
| `docs/05.plans/` | `docs/04.execution/plans/` |
| `docs/06.tasks/` | `docs/04.execution/tasks/` |
| `docs/07.guides/` | `docs/05.operations/guides/` |
| `docs/07.operations/` | `docs/05.operations/guides/` |
| `docs/08.operations/` | `docs/05.operations/policies/` |
| `docs/09.runbooks/` | `docs/05.operations/runbooks/` |
| `docs/10.incidents/` | `docs/05.operations/incidents/` |

이 표는 과거 경로 해석을 돕기 위한 compatibility note입니다. 새 active artifact는 반드시 새 경로에 작성합니다.

## How to Work in This Area

1. 새 문서를 만들기 전에 이 README와 대상 stage의 `README.md`를 먼저 읽습니다.
2. 새 active stage 문서는 반드시 위 Structure에 나열된 canonical 경로 아래에 둡니다.
3. 새 문서는 [99.templates](99.templates/README.md)의 대응 템플릿을 사용하고, README는 [99.templates/readme.template.md](99.templates/readme.template.md)를 따릅니다.
4. 문서 변경 후 상위 README, 관련 stage 문서, traceability 링크를 함께 갱신합니다.
5. secret 값, token, 인증서 원문은 문서에 쓰지 않습니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작합니다.
- 기존 SSoT 문서를 중복 생성하지 않습니다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성합니다.
- 상위 문서와 하위 산출물 간 추적성을 유지합니다.
- Agent 전용 문서(`docs/00.agent-governance/`, `AGENTS.md` 등)는 영어를 원칙으로 하고, 사람 대상 README/operations/reference 문서는 한국어를 기본으로 합니다.
- `docs/03.specs/**`, `docs/04.execution/plans/**`, `docs/04.execution/tasks/**`의 leaf 문서는 영어로 작성합니다.
- `docs/05.operations/{guides,policies,runbooks,incidents}/**`는 한국어 본문을 기본으로 하되 command, path, service name, Docker profile, environment variable, secret ID, evidence label은 원문을 보존합니다.
- Markdown 링크는 상대 경로를 사용하며 절대 경로나 `file://`를 사용하지 않습니다.

| Surface | Language Rule |
| --- | --- |
| `00.agent-governance/` | English-only governance, provider, rule, scope, and memory contracts |
| `01.requirements/` | 한국어 기본, technical identifier와 acceptance criteria 구조 보존 |
| `02.architecture/` | 한국어 설명과 English decision ID/title/quality attribute를 함께 보존 |
| `03.specs/` | English-only technical specifications and contracts |
| `04.execution/plans/` | English-only implementation plans |
| `04.execution/tasks/` | English-only task evidence |
| `05.operations/guides/` | 한국어 usage guidance, commands/paths/service names 원문 보존 |
| `05.operations/policies/` | 한국어 operational controls, control/evidence identifiers 원문 보존 |
| `05.operations/runbooks/` | 한국어 procedures, commands/expected outputs/escalation evidence 원문 보존 |
| `05.operations/incidents/` | 한국어 incident narrative, timestamps/IDs/commands/evidence labels 원문 보존 |
| `90.references/` | 대상 독자 기준: LLM/generated index는 English 가능, 사람 대상 reference는 한국어 기본 |
| `98.archive/` | 간결한 tombstone 기록, original path/date/title/replacement 원문 보존 |
| `99.templates/` | target stage 언어 규칙을 따르며 template README는 한국어 기본 |

## Documentation Contract

| Stage | Responsibility | Template |
| --- | --- | --- |
| `01.requirements/` | 문제, 사용자 가치, scope, acceptance criteria | `99.templates/prd.template.md` |
| `02.architecture/requirements/` | 시스템 경계, 품질 속성, 참조 아키텍처 | `99.templates/ard.template.md` |
| `02.architecture/decisions/` | 선택, 대안, consequence를 남기는 결정 기록 | `99.templates/adr.template.md` |
| `03.specs/` | 구현 계약, interface, data/config contract, verification | `99.templates/spec.template.md` |
| `04.execution/plans/` | 실행 순서, risk control, verification plan | `99.templates/plan.template.md` |
| `04.execution/tasks/` | 실제 수행 상태, evidence, deviation, completion record | `99.templates/task.template.md` |
| `05.operations/` | guide, policy, runbook, incident/postmortem | `99.templates/guide.template.md`, `99.templates/policy.template.md`, `99.templates/runbook.template.md`, incident/postmortem templates |
| `90.references/` | active 판단을 대체하지 않는 stable reference | `99.templates/reference.template.md` |
| `98.archive/` | active chain에서 제거된 old 문서 tombstone | `99.templates/archive.template.md` |
| `99.templates/` | canonical template source and target-relative link rules | `99.templates/readme.template.md` |

문서 lifecycle은 requirement → architecture → specification → execution → operations 순서로 흐릅니다. Reference는 lifecycle을 보조하고, template은 lifecycle 문서의 구조와 링크 계산 기준을 제공합니다.

## Cross-link Rules

- 새 문서와 갱신 문서는 하나의 `## Related Documents` 섹션을 유지합니다.
- 상대 링크는 현재 파일 위치 기준으로 계산합니다.
- 템플릿의 예시 링크는 복사된 target 위치에서 다시 계산한 뒤 실제 문서 경로로 바꿉니다.
- README는 폴더 index이므로 파일 추가, 이동, 삭제가 있으면 parent README를 함께 갱신합니다.
- 오래된 문서를 archive/reference로 옮기거나 삭제하려면 먼저 참조 검색과 migration note가 필요합니다.
- 현재 구현과 상충하는 whole-document old 문서는 `98.archive/` tombstone으로 이동하고 active 문서에서는 archive로 역링크하지 않습니다.

## Template Usage

| 문서 유형 | 위치 | 템플릿 |
| --- | --- | --- |
| Requirements | `01.requirements/` | `99.templates/prd.template.md` |
| Architecture Requirements | `02.architecture/requirements/` | `99.templates/ard.template.md` |
| Architecture Decision | `02.architecture/decisions/` | `99.templates/adr.template.md` |
| Spec | `03.specs/` | `99.templates/spec.template.md` |
| API Spec | feature directory `api-spec.md` | `99.templates/api-spec.template.md` |
| Agent Design | feature directory `agent-design.md` | `99.templates/agent-design.template.md` |
| Data Model | feature directory `data-model.md` | `99.templates/data-model.template.md` |
| Test Contract | feature directory `tests.md` | `99.templates/tests.template.md` |
| OpenAPI Contract | feature directory `contracts/openapi.yaml` | `99.templates/openapi.template.yaml` |
| GraphQL Contract | feature directory `contracts/schema.graphql` | `99.templates/schema.template.graphql` |
| Protobuf Contract | feature directory `contracts/service.proto` | `99.templates/service.template.proto` |
| Plan | `04.execution/plans/` | `99.templates/plan.template.md` |
| Task | `04.execution/tasks/` | `99.templates/task.template.md` |
| Operations Guide | `05.operations/guides/` | `99.templates/guide.template.md` |
| Operations Policy | `05.operations/policies/` | `99.templates/policy.template.md` |
| Runbook | `05.operations/runbooks/` | `99.templates/runbook.template.md` |
| Incident | `05.operations/incidents/` | `99.templates/incident.template.md` |
| Postmortem | `05.operations/incidents/` | `99.templates/postmortem.template.md` |
| Reference | `90.references/` | `99.templates/reference.template.md` |
| Archive Tombstone | `98.archive/` | `99.templates/archive.template.md` |
| README | 각 폴더 | `99.templates/readme.template.md` |

템플릿 없이 새 형식을 임의로 추가하기 전에 기존 문서 체계를 먼저 검토합니다. 동일 목적의 문서가 이미 존재하면 새 문서를 만들기보다 기존 문서를 확장하는 방식을 우선합니다.

## Document Contract Validation

문서 체계와 repository contract는 다음 검증으로 유지합니다.

```bash
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
```

`check-repo-contracts.sh`는 허용된 docs top-level 폴더, required README, template inventory, GitHub Actions YAML, script references, Docker image tag policy, tech-stack version drift, runtime agent/function catalog, LLM Wiki contract 동기화와 generated index freshness를 확인합니다. `check-doc-traceability.sh`는 execution plans와 operations 문서 간 추적성 동기화를 확인합니다.

## Current Refresh Evidence

현재 infra/secrets/docs refresh 작업은 기존 spec/plan/task 문서를 새 taxonomy 안에서 in-place로 재사용합니다.

| Evidence | Current State |
| --- | --- |
| Spec | [03.specs/infra-secrets-docs-refresh/spec.md](03.specs/infra-secrets-docs-refresh/spec.md) |
| Plan | [04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md](04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md) |
| Task evidence | [04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md](04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md) |
| Runtime scope | Docker Compose runtime, secret values, cert contents, agent runtime unchanged |

## Current LLM Wiki Evidence

| Evidence | Current State |
| --- | --- |
| Spec | [03.specs/llm-wiki-agent-first-completion/spec.md](03.specs/llm-wiki-agent-first-completion/spec.md) |
| Plan | [04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md](04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md) |
| Task evidence | [04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md](04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md) |
| Repository map | [90.references/llm-wiki/repository-map.md](90.references/llm-wiki/repository-map.md) |
| Generated index | [90.references/llm-wiki/index.md](90.references/llm-wiki/index.md) |
| Operations guide | [05.operations/guides/90-knowledge/llm-wiki-maintenance.md](05.operations/guides/90-knowledge/llm-wiki-maintenance.md) |

## Related Documents

- [00.agent-governance/README.md](00.agent-governance/README.md)
- [01.requirements/README.md](01.requirements/README.md)
- [02.architecture/README.md](02.architecture/README.md)
- [03.specs/README.md](03.specs/README.md)
- [04.execution/README.md](04.execution/README.md)
- [05.operations/README.md](05.operations/README.md)
- [90.references/README.md](90.references/README.md)
- [90.references/llm-wiki/README.md](90.references/llm-wiki/README.md)
- [90.references/llm-wiki/repository-map.md](90.references/llm-wiki/repository-map.md)
- [90.references/llm-wiki/index.md](90.references/llm-wiki/index.md)
- [98.archive/README.md](98.archive/README.md)
- [99.templates/README.md](99.templates/README.md)
- [../README.md](../README.md)
- [../infra/README.md](../infra/README.md)
- [../secrets/README.md](../secrets/README.md)
- [../scripts/README.md](../scripts/README.md)
