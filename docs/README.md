---
title: "Documentation Space"
version: "1.1.1"
type: "common/documentation-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
---

# docs

> Shared harness-engineering and agent-first engineering documentation space for staged repository knowledge.

## Overview

`docs/`는 shared harness-engineering and agent-first engineering 목적에 맞춰 프로젝트의 요구사항, 아키텍처, 결정 사항, 기술 명세, 실행 증거, 운영 지식을 통합 관리하는 표준 공간입니다. 활성 문서는 허용된 taxonomy 안에서만 관리하며, 검증 스크립트가 이 계약을 강제합니다.

현재 문서 흐름은 `01.requirements -> 02.architecture -> 03.specs -> 05.operations`입니다. Plan과 Task는 별도 stage가 아니라 소유 패키지 안의 `03.specs/{number:4}-{slug}/plan.md`와 `03.specs/{number:4}-{slug}/tasks/`에 함께 놓입니다. 보조 공간으로 `00.agent-governance`, `90.references`, `98.archive`, `99.templates`를 사용합니다.

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
├── 02.architecture/            # 아키텍처 설명과 결정 기록
│   ├── descriptions/
│   └── decisions/
├── 03.specs/                   # Spec Package: spec, plan, tasks, contracts 동거
│   └── ####-<slug>/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks/
│       └── contracts/
├── 05.operations/              # 운영 가이드, 정책, 런북, 사고 기록
│   ├── catalog/<domain>/####-<subject>/
│   └── incidents/<year>/inc-####-<slug>/
├── 90.references/              # 느리게 변하는 참고 지식, 표준, 학습 로드맵, LLM Wiki
├── 98.archive/                 # frozen preserved bodies plus migration/tombstone disposition records
├── 99.templates/               # stage 문서 작성을 위한 표준 템플릿
└── README.md                   # This file
```

## Routing

| I need to... | Go to |
| --- | --- |
| define user value or requirements | `01.requirements/` |
| describe architecture | `02.architecture/descriptions/` |
| record an architecture decision | `02.architecture/decisions/` |
| write a technical specification | `03.specs/####-<slug>/spec.md` |
| declare an executable interface contract | `03.specs/####-<slug>/contracts/` |
| plan implementation work | `03.specs/####-<slug>/plan.md` |
| record task evidence | `03.specs/####-<slug>/tasks/` |
| operate or configure a service | `05.operations/catalog/` |
| define operational controls | `05.operations/catalog/` |
| execute recovery or repeatable procedures | `05.operations/catalog/` |
| record incidents or postmortems | `05.operations/incidents/<year>/inc-####-<slug>/` |
| provide LLM-facing repository navigation | `90.references/data/0082-llm-wiki-index/` |
| inspect a preserved body or its disposition record | `98.archive/` |

## Migration Map

이전 stage 경로의 이관 매핑은 [Stage 98 README](98.archive/README.md)를
통해 historical Migration에서 찾습니다. 그 기록은 과거 이동의 근거이며
현재 경로나 작성 계약은 Stage 99 Registry가 소유합니다.

## How to Work in This Area

1. 새 문서를 만들기 전에 이 README와 대상 stage의 `README.md`를 먼저 읽습니다.
2. 새 active stage 문서는 반드시 위 Structure에 나열된 canonical 경로 아래에 둡니다.
3. 새 문서는 [99.templates](99.templates/README.md)의 대응 템플릿을 사용하고, README는 [99.templates/templates/common/readme-documentation.template.md](99.templates/templates/common/readme-documentation.template.md)를 따릅니다.
4. 문서 변경 후 상위 README, 관련 stage 문서, traceability 링크를 함께 갱신합니다.
5. secret 값, token, 인증서 원문은 문서에 쓰지 않습니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작합니다.
- 기존 SSoT 문서를 중복 생성하지 않습니다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성합니다.
- 상위 문서와 하위 산출물 간 추적성을 유지합니다.
- Agent 전용 문서(`docs/00.agent-governance/`, `AGENTS.md` 등)는 영어를 원칙으로 하고, 사람 대상 README/operations/reference 문서는 한국어를 기본으로 합니다.
- `docs/03.specs/**`의 leaf 문서는 영어로 작성합니다. 여기에는 같은 패키지 안의 `plan.md`와 `tasks/**`가 포함됩니다.
- `docs/05.operations/catalog/**`와 `docs/05.operations/incidents/**`는 한국어 본문을 기본으로 하되 command, path, service name, Docker profile, environment variable, secret ID, evidence label은 원문을 보존합니다.
- Markdown 링크는 상대 경로를 사용하며 절대 경로나 `file://`를 사용하지 않습니다.

| Surface | Language Rule |
| --- | --- |
| `00.agent-governance/` | English-only governance, provider, rule, scope, and memory contracts |
| `01.requirements/` | 한국어 기본, technical identifier와 acceptance criteria 구조 보존 |
| `02.architecture/` | 한국어 설명과 English decision ID/title/quality attribute를 함께 보존 |
| `03.specs/` | English-only technical specifications and contracts |
| `03.specs/####-<slug>/plan.md` | English-only implementation plans |
| `03.specs/####-<slug>/tasks/` | English-only task evidence |
| `05.operations/catalog/` | 한국어 guide/policy/runbook, commands/paths/service names 원문 보존 |
| `05.operations/incidents/` | 한국어 incident narrative, timestamps/IDs/commands/evidence labels 원문 보존 |
| `90.references/` | 대상 독자 기준: LLM/generated index는 English 가능, 사람 대상 reference는 한국어 기본 |
| `98.archive/` | frozen 원문 보존; 현재 README와 migration/tombstone의 기록 계약은 분리 |
| `99.templates/` | target stage 언어 규칙을 따르며 template README는 한국어 기본 |

## Documentation Contract

[Stage 99](99.templates/README.md) owns all document profiles, paths, lifecycle,
identifiers, and registered templates. [Stage 00](00.agent-governance/README.md)
owns authoring behavior and approval boundaries. This index is navigation only.

## Cross-link Rules

- 새 문서와 갱신 문서는 하나의 `## Related Documents` 섹션을 유지합니다.
- 상대 링크는 현재 파일 위치 기준으로 계산합니다.
- 템플릿의 예시 링크는 복사된 target 위치에서 다시 계산한 뒤 실제 문서 경로로 바꿉니다.
- README는 폴더 index이므로 파일 추가, 이동, 삭제가 있으면 parent README를 함께 갱신합니다.
- Archive/delete 후보는 [Stage 99 계약](99.templates/README.md)과 [Stage 00 승인 경계](00.agent-governance/policies/approval-boundaries.md)에 따라 분류하고, 검증된 Git 복구 근거와 독립 검토를 남깁니다.
- `completed/`와 `superseded/` 보존본은 역사적 증거로 직접 인용할 수 있지만,
  같은 문맥에서 현재 Stage 00/01/02/05 소유자를 함께 연결해야 합니다.
  `retired/`, Tombstone, Migration은 현재 권위의 의존성이 아니며 Stage 98
  README를 통해 탐색합니다.

## Template Usage

Select the role in the [Registry](99.templates/registry.json) and copy its source
from the [template catalog](99.templates/templates/README.md). Spec, Plan, Task,
and machine contracts are co-located in Stage 03. Requirement child identities
are owned by their package; Stage 98 contains frozen preserved bodies and their
separate migration or tombstone disposition records.

## Document Contract Validation

문서 체계와 repository contract는 다음 검증으로 유지합니다.

```bash
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/check-document-links.py --mode traceability
```

`run-ci-gate.py`는 허용된 docs top-level 폴더, required README, template inventory, GitHub Actions YAML, script references, Docker image tag policy, tech-stack version drift, runtime agent/function catalog, LLM Wiki contract 동기화와 generated index freshness를 확인합니다. `check-document-links.py --mode alignment`은 현재 소유자 문서와 operations 문서 간 추적성 동기화를 확인합니다.

## Historical Refresh Evidence

이전 infra/secrets/docs refresh의 실행 기록은 아래 보존 package에 있습니다.
현재 구조와 운영 안내는 [infra README](../infra/README.md)와
[Operations](05.operations/README.md)가 소유하며 완료 package를 새 작업 기록으로
재사용하지 않습니다.

<!-- Historical evidence table (not current authority; source: Git history). -->

| Evidence | Current State |
| --- | --- |
| Spec | [03.specs/0095-infra-secrets-docs-refresh/spec.md](98.archive/completed/03.specs/0095-infra-secrets-docs-refresh/spec.md) |
| Plan and Task evidence | co-located in the owning Spec Package |
| Runtime scope | Docker Compose runtime, secret values, cert contents, agent runtime unchanged |

## LLM Wiki Ownership and Historical Evidence

| Evidence | Current State |
| --- | --- |
| Historical implementation | [SPEC-0096](98.archive/completed/03.specs/0096-llm-wiki-agent-first-completion/spec.md); current procedure: [LLM Wiki guide](05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md) |
| Plan and Task evidence | co-located in the owning Spec Package |
| Repository map | [90.references/data/0083-repository-map/README.md](90.references/data/0083-repository-map/README.md) |
| Generated index | [90.references/data/0082-llm-wiki-index/README.md](90.references/data/0082-llm-wiki-index/README.md) |
| Operations guide | [05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md](./05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md) |

## Related Documents

- [00.agent-governance/README.md](00.agent-governance/README.md)
- [01.requirements/README.md](01.requirements/README.md)
- [02.architecture/README.md](02.architecture/README.md)
- [03.specs/README.md](03.specs/README.md)
- [05.operations/README.md](05.operations/README.md)
- [90.references/README.md](90.references/README.md)
- [90.references/data/0082-llm-wiki-index/README.md](90.references/data/0082-llm-wiki-index/README.md)
- [90.references/data/0083-repository-map/README.md](90.references/data/0083-repository-map/README.md)
- [98.archive/README.md](98.archive/README.md)
- [99.templates/README.md](99.templates/README.md)
- [../README.md](../README.md)
- [../infra/README.md](../infra/README.md)
- [../secrets/README.md](../secrets/README.md)
- [../scripts/README.md](../scripts/README.md)
