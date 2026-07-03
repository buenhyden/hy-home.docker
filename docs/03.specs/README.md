---
status: active
---

<!-- Target: docs/03.specs/README.md -->

# 03.specs

> 컴포넌트와 기능별 기술 명세, 구현 계약, 검증 기준을 관리하는 stage

## Overview

`docs/03.specs`는 PRD, ARD, ADR을 구현 가능한 기술 계약으로 바꾸는 stage입니다. 각 spec은 구현자가 무엇을 바꾸고, 어떤 interface와 data contract를 지켜야 하며, 어떤 검증으로 완료를 판단할지 설명합니다.

이 경로는 계획이나 작업 증거를 보관하지 않습니다. 실행 순서와 위험 관리는 `docs/04.execution/plans/`, 작업 결과와 evidence는 `docs/04.execution/tasks/`, 운영 절차와 정책은 `docs/05.operations/`가 담당합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- AI Agents
- QA Engineers

## Scope

### In Scope

- 컴포넌트/기능별 technical specification
- config, data/interface, governance contract
- API, schema, proto, tests, data model 같은 spec child contract
- AI Agent 역할, tool, guardrail, evaluation contract
- 구현 전 검증 기준과 성공 조건

### Out of Scope

- 제품 요구사항과 사용자 가치 정의 (`docs/01.requirements/` 담당)
- 아키텍처 요구사항과 의사결정 (`docs/02.architecture/` 담당)
- 구현 순서, milestone, 작업 배분 (`docs/04.execution/plans/` 담당)
- 작업 수행 evidence (`docs/04.execution/tasks/` 담당)
- 운영 가이드, 정책, 런북 (`docs/05.operations/` 담당)
- Docker Compose runtime 원문이나 secret 값

## Structure

```text
docs/03.specs/
├── 01-gateway/                          # Traefik/Nginx gateway contracts
├── 02-auth/                             # Keycloak/OAuth2 Proxy contracts
├── 03-security/                         # Vault and secret delivery contracts
├── 04-data/                             # Core data service contracts
├── 04-data-analytics/                   # Analytics engine contracts
├── 05-messaging/                        # Kafka/RabbitMQ messaging contracts
├── 06-observability/                    # LGTM observability contracts
├── 07-workflow/                         # Airflow/n8n workflow contracts and agent design
├── 08-ai/                               # Ollama/Open WebUI AI contracts
├── 09-tooling/                          # Tooling service contracts
├── 10-communication/                    # Mail communication contracts
├── 11-laboratory/                       # Laboratory/admin surface contracts
├── document-restructure-audit-contract-archive/ # Draft second-wave document restructure design spec
├── docs-taxonomy-agent-first-migration/ # Completed docs taxonomy migration spec
├── agentic-engineering-implementation-audit-pack/ # Draft Stage 90 audit pack design spec
├── harness-agent-first-engineering/     # Completed agent-first harness spec
├── home-docker-revalidation-deferred-follow-up/ # Completed Home Docker revalidation and deferred-follow-up spec
├── infra-secrets-docs-refresh/          # Completed infra/secrets/docs refresh spec
├── llm-wiki-agent-first-completion/     # Completed LLM Wiki contract spec
├── standardize-infra-net/               # Completed infra_net standardization spec
├── template-system-contract-standardization/ # Draft Stage 99 contract/frontmatter standardization spec
├── template-system-reorganization/      # Draft Stage 99 template system reorganization spec
├── workspace-document-contract-audit-pack/ # Active workspace document contract audit pack spec
├── workspace-audit-2026-05/             # Completed 2026-05-26 workspace audit historical spec
├── workspace-doc-consistency-2026-05/   # Completed 2026-05-28 workspace doc consistency spec (PR #89)
├── workspace-consistency-2026-05b/      # Completed 2026-05-29 workspace governance consistency follow-up spec
└── README.md                            # This file
```

## Routing

| If you need to define...                                   | Use                                                  |
| ---------------------------------------------------------- | ---------------------------------------------------- |
| Gateway routing, TLS, middleware, proxy behavior           | `01-gateway/spec.md`                                 |
| Identity, OAuth2, OIDC, session store behavior             | `02-auth/spec.md`                                    |
| Vault, secret template, AppRole, secret delivery behavior  | `03-security/spec.md`                                |
| Databases, cache, object storage, core data persistence    | `04-data/spec.md`                                    |
| InfluxDB, ksqlDB, OpenSearch, OLAP analytics engines       | `04-data-analytics/spec.md`                          |
| Kafka, RabbitMQ, stream/message broker behavior            | `05-messaging/spec.md`                               |
| Metrics, logs, traces, dashboards, alerts                  | `06-observability/spec.md`                           |
| Workflow orchestration and cross-validation agent behavior | `07-workflow/spec.md`, `07-workflow/agent-design.md` |
| Agentic engineering reference-audit pack design            | `agentic-engineering-implementation-audit-pack/spec.md` |
| Second-wave document restructure audit, contract, and archive design | `document-restructure-audit-contract-archive/spec.md` |
| Stage 99 template taxonomy and reorganization design | `template-system-reorganization/spec.md` |
| Stage 99 template contract and frontmatter standardization design | `template-system-contract-standardization/spec.md` |
| Workspace-wide document contract audit and normalization design | `workspace-document-contract-audit-pack/spec.md` |
| Local AI inference, RAG UI, model-serving contracts        | `08-ai/spec.md`, `08-ai/open-webui.md`               |
| IaC, registry, quality, performance tooling services       | `09-tooling/spec.md`                                 |
| Mail, SMTP, IMAP, development mail trapping                | `10-communication/spec.md`                           |
| Laboratory/admin UI surfaces and access contracts          | `11-laboratory/spec.md`                              |
| Completed governance/documentation contract work           | named governance spec folders                        |

## How to Work in This Area

1. 새 spec을 만들기 전에 상위 PRD, ARD, ADR이 있는지 확인합니다.
2. 새 `spec.md`는 [spec template](../99.templates/templates/sdlc/spec.template.md)을 복사해 작성합니다.
3. README는 [README template](../99.templates/templates/common/readme.template.md)을 기준으로 작성하고, 링크는 대상 README 위치 기준으로 계산합니다.
4. Agent 전용 설계가 필요하면 [agent design template](../99.templates/templates/spec-contracts/agent-design.template.md)을 사용해 해당 feature 디렉터리의 `agent-design.md`에 둡니다.
5. API, schema, proto, tests, data model 계약은 같은 feature 디렉터리 아래 child document로 둡니다.
6. `## Related Documents`는 실제 Markdown 링크로 작성합니다. 문서 경로를 코드 span 안에만 남기지 않습니다.
7. 운영 링크는 목적별 bucket을 맞춥니다: guide는 `docs/05.operations/guides/`, policy는 `docs/05.operations/policies/`, runbook은 `docs/05.operations/runbooks/`.
8. 이미지 태그, 고정 IP, 포트 같은 구현값 예시는 tracked compose와 `infra/tech-stack.versions.json`에 맞는 실제 값을 사용하고, 복사 가능한 placeholder를 남기지 않습니다.

## Spec Contract

Spec은 구현자가 따라야 하는 기술 계약입니다. 요구사항이나 실행 evidence를 다시 쓰지 않고, 다음 항목을 구현 가능한 형태로 연결합니다.

| Contract Area      | Expected Content                                |
| ------------------ | ----------------------------------------------- |
| Related inputs     | PRD, ARD, ADR 링크 또는 명시적인 부재 사유      |
| Contracts          | config, data/interface, governance contract     |
| Core design        | component boundary, dependencies, stack         |
| Verification       | 실행 가능한 명령, 수동 확인 기준, pass criteria |
| Operations handoff | guide, policy, runbook 중 실제 운영 target 링크 |

API, data model, tests, agent design 같은 child document는 같은 feature 디렉터리에 둡니다. 실행 순서와 작업 evidence는 `docs/04.execution`으로 연결합니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.
- 기존 spec의 domain facts를 보존하고, template section을 보강할 때 의미를 바꾸지 않는다.
- ordinary broken-link 검사뿐 아니라 pseudo-link와 label/path mismatch를 확인한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 코드 변경 전 이 영역의 스펙 문서를 우선 참조하여 설계 의도를 파악한다.
3. Graphify는 탐색 보조로만 사용하고, spec 판단은 tracked source files와 stage docs로 확인한다.
4. 스펙과 실제 구현 사이의 불일치를 발견하면 즉시 보고하거나 문서를 수정한다.
5. 새 PRD/ARD/ADR/Plan/Task가 필요한 변경이면 해당 stage template으로 별도 작성하고, 이 경로에 대체 문서를 만들지 않는다.

## Stage Handoff

이 stage의 완료 기준이 충족되면 [`docs/04.execution/`](../04.execution/README.md)로 이관한다. 구현 순서와 risk control은 `plan.template.md`를 사용해 Plan 문서로, 작업 수행 evidence는 `task.template.md`를 사용해 Task 문서로 기록한다. 상세 매핑은 [`stage-authoring-matrix.md`](../00.agent-governance/rules/stage-authoring-matrix.md)를 따른다.

## Related Documents

- **PRD**: [../01.requirements/README.md](../01.requirements/README.md)
- **ARD**: [../02.architecture/requirements/README.md](../02.architecture/requirements/README.md)
- **ADR**: [../02.architecture/decisions/README.md](../02.architecture/decisions/README.md)
- **Plan**: [../04.execution/plans/README.md](../04.execution/plans/README.md)
- **Tasks**: [../04.execution/tasks/README.md](../04.execution/tasks/README.md)
- **Operations Stage**: [../05.operations/README.md](../05.operations/README.md)
- **Spec template**: [../99.templates/templates/sdlc/spec.template.md](../99.templates/templates/sdlc/spec.template.md)
- **README template**: [../99.templates/templates/common/readme.template.md](../99.templates/templates/common/readme.template.md)
- **Agentic Engineering Implementation Audit Pack Spec**: [agentic-engineering-implementation-audit-pack/spec.md](./agentic-engineering-implementation-audit-pack/spec.md)
- **Document Restructure Audit, Contract, and Archive Spec**: [document-restructure-audit-contract-archive/spec.md](./document-restructure-audit-contract-archive/spec.md)
- **Harness / Agent-first Engineering Spec**: [harness-agent-first-engineering/spec.md](./harness-agent-first-engineering/spec.md)
- **Home Docker Revalidation Deferred Follow-up Spec**: [home-docker-revalidation-deferred-follow-up/spec.md](./home-docker-revalidation-deferred-follow-up/spec.md)
- **Infra / Secrets / Docs Refresh Spec**: [infra-secrets-docs-refresh/spec.md](./infra-secrets-docs-refresh/spec.md)
- **LLM Wiki Agent-first Completion Spec**: [llm-wiki-agent-first-completion/spec.md](./llm-wiki-agent-first-completion/spec.md)
- **Template System Reorganization Spec**: [template-system-reorganization/spec.md](./template-system-reorganization/spec.md)
- **Template System Contract Standardization Spec**: [template-system-contract-standardization/spec.md](./template-system-contract-standardization/spec.md)
- **Workspace Document Contract Audit Pack Spec**: [workspace-document-contract-audit-pack/spec.md](./workspace-document-contract-audit-pack/spec.md)
- **Workspace Audit 2026-05 Spec**: [workspace-audit-2026-05/spec.md](./workspace-audit-2026-05/spec.md)
