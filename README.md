# hy-home.docker

> Shared harness-engineering and agent-first engineering workspace for modular Docker Compose home infrastructure.

## Overview

`hy-home.docker`는 shared harness-engineering and agent-first engineering workspace로, 홈 서버와 개인 개발 인프라를 Docker Compose 중심으로 표준화하고 그 위에 요구사항, 설계, 계획, 작업, 운영 지식을 단계별 문서 체계로 연결하는 저장소입니다. 루트 [`docker-compose.yml`](./docker-compose.yml)은 `infra/**/docker-compose*.yml` 파일을 `include`로 통합해 단일 진입점 역할을 수행합니다.

이 저장소의 핵심 목적은 다음 세 가지입니다. 첫째, 인프라 구성을 계층별로 분리해 서비스 추가와 변경 영향을 명확히 만드는 것. 둘째, 문서와 실행 대상을 연결해 추적성과 검증 가능성을 확보하는 것. 셋째, AI Agent와 사람이 동일한 규칙 아래에서 안전하게 협업할 수 있도록 진입 규칙과 작업 범위를 명확히 유지하는 것입니다.

## Audience

이 README의 주요 독자:

- 인프라 운영자
- 개발자 및 서비스 소비자
- 문서 작성자
- AI Agents

## Scope

### In Scope

- 루트 Docker Compose 진입점과 계층별 인프라 구조 안내
- 문서 체계와 거버넌스 진입 경로 안내
- 로컬 환경 준비, 사전 점검, 구성 검증, 기본 실행 절차
- 검증 스크립트와 CI 품질 게이트의 역할 요약

### Out of Scope

- 개별 서비스의 세부 설정과 운영 절차
- 비밀값 자체, 자격 증명, 토큰, 인증서 원문
- 애플리케이션 비즈니스 로직이나 서비스 내부 구현 설명
- 사용자의 명시적 지시 없이 공식 stage 문서를 수정하는 작업

## Structure

```text
hy-home.docker/
├── docs/                 # 00.agent-governance, 01~05, 90, 99 공식 문서 체계
├── infra/                # 계층별 Docker Compose 서비스 정의
├── scripts/              # 사전 점검, 검증, 자동화 스크립트
├── secrets/              # Docker secrets 및 민감 정보 매핑
├── projects/             # 보조 프로젝트 및 예제 작업 공간
├── tests/                # 테스트 관련 문서와 자산
├── docker-compose.yml    # 통합 Compose 진입점
├── llms.txt              # LLM용 repo-local 탐색 진입점
├── .env.example          # 환경 변수 예시
├── AGENTS.md             # Agent 진입 규칙
└── README.md             # 이 문서
```

## Repository Map

- [`docs/`](./docs) - 요구사항, 아키텍처, 명세, 실행, 운영 지식까지 포함하는 공식 문서 체계
- [`docs/05.operations/`](./docs/05.operations) - 사용 가이드, 운영 정책, 런북, 사고 기록을 분리해 관리하는 운영 지식 베이스
- [`docs/90.references/`](./docs/90.references) - Docker, 학습 로드맵 등 느리게 변하는 참고 지식
- [`llms.txt`](./llms.txt) - LLM 에이전트용 repo-local 탐색 진입점
- [`docs/90.references/llm-wiki/`](./docs/90.references/llm-wiki) - tracked source files 기반 LLM Wiki entrypoint
- [`docs/90.references/llm-wiki/repository-map.md`](./docs/90.references/llm-wiki/repository-map.md) - curated repository map
- [`docs/90.references/llm-wiki/index.md`](./docs/90.references/llm-wiki/index.md) - generated tracked path index
- [`infra/`](./infra) - `01-gateway`부터 `11-laboratory`까지 계층별 서비스 정의
- [`scripts/`](./scripts) - 사전 점검, Compose 검증, 하드닝/추적성 검사 스크립트
- [`secrets/`](./secrets) - Docker secrets 파일 구조와 민감 정보 관리 기준
- [`projects/`](./projects) - 보조 앱, 스토리북, MCP 관련 프로젝트 공간
- [`.github/workflows/`](.github/workflows) - repository contract, Git flow, Compose, 하드닝, pre-commit, 보안 검사를 수행하는 CI 정의
- [`docs/90.references/docker/`](./docs/90.references/docker) - Docker image/version drift 기준과 참고 규칙
- [`docs/03.specs/infra-secrets-docs-refresh/`](./docs/03.specs/infra-secrets-docs-refresh) - infra, secrets, 운영 문서 최신화 분석 명세

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Orchestration | Docker Compose | 루트 `include` 기반 통합 실행 |
| Infrastructure | 계층형 Compose 스택 | `infra/01`~`infra/11` 서비스 정의 |
| Documentation | Markdown + stage-based docs | `docs/00`, `docs/01`~`docs/05`, `docs/90`, `docs/99` |
| Automation | Bash scripts | 사전 점검, 검증, 하드닝, 추적성 검사 |
| CI / Quality | GitHub Actions + pre-commit + zizmor | 문서/보안/품질 게이트 자동화 |
| Version Drift Gate | [`infra/tech-stack.versions.json`](./infra/tech-stack.versions.json) | 주요 Docker image 선언과 Compose source of truth 동기화 |

## Current Infrastructure Snapshot

현재 문서 갱신 기준의 운영 인벤토리는 다음과 같습니다.

| Area | Current Evidence | Notes |
| --- | --- | --- |
| `infra/` Compose files | 48 | `docker-compose*.yml`과 `docker-compose*.yaml`를 함께 계산하며, 루트 Compose 활성 include와 standalone/variant Compose를 구분해야 함 |
| `infra/` Compose service directories | 40 | service README 누락 0개 |
| Root active includes | 17 | 주석 처리된 optional include는 실행면으로 과장하지 않음 |
| Root Compose secret declarations | 69 | 선언된 secret 파일 누락 0개 |
| `secrets/` value/cert files | 94 | 값은 열람하지 않고 파일명과 경로만 기준으로 분류 |
| Parent-repo tracked README files | 173 | `git ls-files '*README.md'` 기준의 tracked README inventory |
| README refresh contract | path-appropriate template coverage | `docs/99.templates/templates/common/readme.template.md`의 공통 구조와 경로별 snippet을 기준으로 갱신 |

## Prerequisites

- Git
- Docker Engine
- Docker Compose v2
- `.env.example`를 기반으로 한 로컬 `.env`
- `secrets/` 아래의 필수 secret 파일과 인증서 파일

## Getting Started

### 1. 저장소 클론

```bash
git clone <repository-url>
cd hy-home.docker
```

### 2. 환경 파일 준비

```bash
cp .env.example .env
```

`.env`에는 마운트 경로, 네트워크 이름, 서비스별 기본 설정이 포함됩니다. 민감값은 `.env`에 직접 하드코딩하지 말고 [`secrets/`](./secrets) 구조를 따릅니다.

### 3. 사전 점검 실행

```bash
bash scripts/validation/validate-docker-compose.sh --preflight
```

이 모드는 `.env`, 필수 secret 파일, 인증서 파일, 주요 디렉터리, 외부 Docker 네트워크 존재 여부를 점검합니다. 일반 Compose 구조 검증과 달리 `.env`, secret 파일, 인증서 파일, dummy 데이터를 만들지 않습니다.

### 4. Compose 구조 검증

```bash
bash scripts/validation/validate-docker-compose.sh
```

이 검증은 기본 `core` profile을 기준으로 `docker compose config`가 성공하는지 확인하고, resolved service count가 0이면 실패합니다. 필요한 경우 `HYHOME_COMPOSE_PROFILES="core dev"`처럼 검증 profile을 명시할 수 있습니다. 검증 스크립트는 누락된 로컬 `.env` 또는 dummy secret 파일을 임시로 만들 수 있으므로, evidence에는 검증 profile과 임시 파일 cleanup 여부를 함께 기록합니다.

### 5. Repository contract 검증

```bash
bash scripts/validation/check-repo-contracts.sh
```

이 검증은 docs taxonomy, required README, template inventory, GitHub Actions YAML, duplicate workflow step, script reference, runtime agent/function catalog, Docker image tag policy, tech-stack version drift를 함께 확인합니다.

### 6. 코어 인프라 실행

```bash
docker compose --profile core up -d
```

기본 코어 계층을 올린 뒤, 필요에 따라 `data`, `obs`, `workflow`, `ai`, `tooling` 같은 프로필을 추가로 활성화할 수 있습니다.

### 7. 주요 진입 문서 확인

1. [`AGENTS.md`](./AGENTS.md) - Agent 작업 진입 규칙
2. [`docs/README.md`](./docs/README.md) - 문서 체계 개요
3. [`docs/00.agent-governance/README.md`](./docs/00.agent-governance/README.md) - 거버넌스 허브
4. [`infra/README.md`](./infra/README.md) - 계층별 인프라 구조
5. [`scripts/README.md`](./scripts/README.md) - 검증 및 자동화 스크립트
6. [`llms.txt`](./llms.txt) - LLM 에이전트용 repo-local 탐색 진입점

## Documentation Standards

이 저장소의 문서는 다음 기준을 따릅니다.

- Agent 전용 규칙 문서는 영어를 사용합니다.
- 루트 `README.md`, 사람이 읽는 폴더 README, 가이드, 운영 문서는 한국어를 기본으로 사용합니다.
- 문서 작성 작업은 가능한 경우 [`docs/99.templates/`](./docs/99.templates)의 템플릿을 출발점으로 사용합니다.
- 상위 문서와 하위 산출물 사이의 추적성을 유지하고, 중복된 SSoT 문서를 만들지 않습니다.

| Surface | Language Rule |
| --- | --- |
| `docs/00.agent-governance/**` | English-only agent governance and policy contracts |
| `docs/01.requirements/**` | 한국어 기본, technical identifier와 acceptance criteria 구조 보존 |
| `docs/02.architecture/**` | 한국어 설명과 English decision ID/title/quality attribute를 함께 보존 |
| `docs/03.specs/**` | English-only technical contracts |
| `docs/04.execution/plans/**` | English-only implementation plans |
| `docs/04.execution/tasks/**` | English-only task evidence |
| `docs/05.operations/{guides,policies,runbooks,incidents}/**` | 한국어 기본, command/path/service/env/evidence label 원문 보존 |
| `docs/90.references/**` | 대상 독자 기준: LLM/generated index는 English 가능, 사람 대상 reference는 한국어 기본 |
| `docs/98.archive/**` | 간결한 tombstone 기록, original path/date/title/replacement 원문 보존 |
| `docs/99.templates/**` | target stage 언어 규칙을 따르며 template README는 한국어 기본 |

## Documentation Lifecycle

문서 stage는 역할이 겹치지 않도록 다음 흐름으로 관리합니다.

| Stage | Responsibility |
| --- | --- |
| [`docs/01.requirements/`](./docs/01.requirements) | 사용자 가치, 문제 정의, 요구사항, 성공 기준 |
| [`docs/02.architecture/`](./docs/02.architecture) | 아키텍처 요구사항과 결정 기록 |
| [`docs/03.specs/`](./docs/03.specs) | 기능별 기술 명세, 인터페이스, 구현 계약 |
| [`docs/04.execution/`](./docs/04.execution) | 실행 계획과 작업 evidence |
| [`docs/05.operations/`](./docs/05.operations) | 운영 가이드, 정책, 런북, 사고 기록 |
| [`docs/90.references/`](./docs/90.references) | 느리게 변하는 참고 지식, 용어, source-backed reference |
| [`docs/99.templates/`](./docs/99.templates) | 새 문서와 README의 canonical template |

일반 작업 흐름은 요구사항 → 아키텍처 → 명세 → 실행 → 운영 순서입니다. 참고 문서는 active stage를 대체하지 않고, 템플릿은 새 문서 작성 전에 target 위치와 상대 링크를 다시 계산하는 기준으로만 사용합니다.

## Common Documentation Workflows

| Workflow | Start Here | Then Update | Verify |
| --- | --- | --- | --- |
| 새 요구사항 정의 | [`docs/01.requirements/README.md`](./docs/01.requirements/README.md) | PRD → ARD/ADR → Spec 링크를 target-relative로 연결 | `bash scripts/validation/check-repo-contracts.sh` |
| 아키텍처 선택 기록 | [`docs/02.architecture/README.md`](./docs/02.architecture/README.md) | ARD 또는 ADR, 관련 Spec 링크 | `bash scripts/validation/check-repo-contracts.sh` |
| 구현 명세 작성 | [`docs/03.specs/README.md`](./docs/03.specs/README.md) | Spec child contracts and execution plan links | `bash scripts/validation/check-repo-contracts.sh` |
| 실행 계획/작업 evidence 갱신 | [`docs/04.execution/README.md`](./docs/04.execution/README.md) | Plan과 Task를 분리하고 검증 evidence 기록 | `bash scripts/validation/check-doc-traceability.sh` |
| 운영 지식 갱신 | [`docs/05.operations/README.md`](./docs/05.operations/README.md) | guide, policy, runbook, incident 목적별 배치 | `bash scripts/validation/check-repo-contracts.sh` |
| 참고 지식 추가 | [`docs/90.references/README.md`](./docs/90.references/README.md) | Reference가 active policy나 runbook을 대체하지 않는지 확인 | `bash scripts/validation/check-repo-contracts.sh` |
| 템플릿 변경 | [`docs/99.templates/README.md`](./docs/99.templates/README.md) | Template-to-folder mapping and target-relative links | `bash scripts/validation/check-repo-contracts.sh` |

새 문서 작업은 항상 해당 stage README에서 시작하고, 생성된 문서의 `## Related Documents` 링크는 템플릿 파일 위치가 아니라 복사된 target 문서 위치 기준으로 다시 계산합니다.

## Agent Working Rules

- 작업 시작 전 [`AGENTS.md`](./AGENTS.md)를 먼저 확인합니다.
- Bootstrap 순서는 `bootstrap.md` → `persona.md` → `task-checklists.md` → `agentic.md` → `memory/README.md`와 `memory/progress.md` review → 해당 scope 순서를 따릅니다.
- 문서 작성/갱신 작업은 [`docs/00.agent-governance/rules/stage-authoring-matrix.md`](./docs/00.agent-governance/rules/stage-authoring-matrix.md)를 기준으로 작성합니다.
- 공식 stage 문서는 기본적으로 읽기 전용이며, 명시적 사용자 지시가 있을 때만 수정합니다.

## Verification and Quality Gates

로컬 또는 CI에서 자주 사용되는 검증 진입점은 다음과 같습니다.

- `bash scripts/validation/validate-docker-compose.sh --preflight` - 실행 전 필수 파일과 디렉터리 점검
- `bash scripts/validation/run-local-qa-gates.sh` - 로컬에서 재현 가능한 script-backed QA/CI 게이트 묶음 실행
- `bash scripts/validation/check-repo-contracts.sh` - repository/docs/GitHub/runtime/Docker/LLM Wiki contract 검증
- `bash scripts/validation/validate-docker-compose.sh` - profile-aware Compose 구조 검증
- `bash scripts/validation/check-doc-traceability.sh` - 문서 추적성 검사
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` - LLM Wiki generated path index freshness 검사
- `bash scripts/validation/check-quickwin-baseline.sh` - QuickWin baseline 검사
- `bash scripts/validation/check-template-security-baseline.sh` - 템플릿 채택 및 필수 보안 baseline 검사
- `bash scripts/hardening/check-all-hardening.sh` - 계층별 하드닝 기준 검사

`pre-commit`은 CI와 hook 정책에서 관리하며, 이 저장소 지시가 바뀌지 않는 한 수동 실행을 기본 절차로 두지 않습니다.

GitHub Actions에서는 다음 품질 게이트를 사용합니다.

- `docs-traceability` - 문서 추적성 검사
- `docs-implementation-alignment` - active docs와 tracked implementation surface 정렬 검사
- `repo-contracts` - docs taxonomy, GitHub workflow, script reference, image/version drift, runtime catalog 검사
- `git-flow-contract` - PR 제목 Conventional Commits와 source branch prefix 검사
- `compose-validation` - Docker Compose 구조 검사
- `compose-all-profiles-validation` - 전체 Compose profile 구조 검사
- `infrastructure-hardening` - 계층별 하드닝 baseline 검사
- `template-security-baseline` - 템플릿/보안 baseline 검사
- `quickwin-baseline` - QuickWin baseline 검사
- `pre-commit` - hook 기반 포맷/린트/품질 검사
- `frontend-quality` - Storybook Next.js lint/typecheck/build/build-storybook 검사
- `storybook-coverage` - Storybook Next.js coverage 검사
- `zizmor` - GitHub Actions 보안 분석

추가로 `v*.*.*` 태그 push에는 `Release Changelog Check`가 실행되어
`CHANGELOG.md`에 해당 release tag 항목이 있는지 확인합니다. 이는 tag-only
release visibility gate이며, remote required-check enforcement 증거로
간주하지 않습니다.

`pre-commit` job은 공통 hook 정책을 CI에서 재현하고, 별도 `zizmor` job은
GitHub Actions 보안 분석 결과를 SARIF로 산출합니다. `stale`, `greetings`,
`pr-labeler` workflow는 필수 품질 게이트가 아니라 triage/community 자동화입니다.
로컬에서는 `bash scripts/validation/run-local-qa-gates.sh --list`로 실행 가능한
script-backed gate와 원격 전용 gate를 구분합니다.

Workflow의 외부 `uses:`는 full commit SHA로 고정하고, 직접 작성한 action step에는 명시적 `name`을 둡니다.

## How to Work in This Area

1. 이 저장소에서 작업을 시작할 때는 먼저 [`AGENTS.md`](./AGENTS.md), [`docs/README.md`](./docs/README.md), [`infra/README.md`](./infra/README.md)를 읽어 전체 구조를 파악합니다.
2. 새 서비스를 추가할 때는 `infra/<tier>/<service>/` 패턴을 따르고, 루트 [`docker-compose.yml`](./docker-compose.yml)의 `include` 및 관련 문서를 함께 검토합니다.
3. 새 문서나 루트 문서를 갱신할 때는 [`docs/99.templates/templates/common/readme.template.md`](./docs/99.templates/templates/common/readme.template.md) 같은 승인된 템플릿과 [`docs/00.agent-governance/rules/documentation-protocol.md`](./docs/00.agent-governance/rules/documentation-protocol.md)을 기준으로 삼습니다.
4. Docker image나 주요 runtime 버전을 바꿀 때는 Compose 선언과 [`infra/tech-stack.versions.json`](./infra/tech-stack.versions.json)을 함께 점검합니다.
5. GitHub workflow를 바꿀 때는 [`docs/00.agent-governance/rules/github-governance.md`](./docs/00.agent-governance/rules/github-governance.md)와 [`docs/00.agent-governance/rules/git-workflow.md`](./docs/00.agent-governance/rules/git-workflow.md)를 기준으로 branch, permission, SHA pinning, step naming을 확인합니다.
6. 변경 후에는 관련 링크, 검증 명령, 문서 정책, CI 영향 범위를 함께 점검하고 필요한 경우 검증 스크립트를 실행합니다.

## Related Documents

- [`docs/README.md`](./docs/README.md)
- [`docs/00.agent-governance/README.md`](./docs/00.agent-governance/README.md)
- [`docs/00.agent-governance/scopes/docs.md`](./docs/00.agent-governance/scopes/docs.md)
- [`docs/00.agent-governance/rules/documentation-protocol.md`](./docs/00.agent-governance/rules/documentation-protocol.md)
- [`docs/00.agent-governance/rules/github-governance.md`](./docs/00.agent-governance/rules/github-governance.md)
- [`docs/00.agent-governance/rules/git-workflow.md`](./docs/00.agent-governance/rules/git-workflow.md)
- [`docs/00.agent-governance/rules/stage-authoring-matrix.md`](./docs/00.agent-governance/rules/stage-authoring-matrix.md)
- [`docs/05.operations/README.md`](./docs/05.operations/README.md)
- [`docs/90.references/README.md`](./docs/90.references/README.md)
- [`docs/90.references/docker/README.md`](./docs/90.references/docker/README.md)
- [`docs/90.references/llm-wiki/README.md`](./docs/90.references/llm-wiki/README.md)
- [`docs/90.references/llm-wiki/index.md`](./docs/90.references/llm-wiki/index.md)
- [`llms.txt`](./llms.txt)
- [`docs/03.specs/infra-secrets-docs-refresh/spec.md`](./docs/03.specs/infra-secrets-docs-refresh/spec.md)
- [`docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md`](./docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md)
- [`infra/README.md`](./infra/README.md)
- [`infra/tech-stack.versions.json`](./infra/tech-stack.versions.json)
- [`scripts/README.md`](./scripts/README.md)
- [`secrets/README.md`](./secrets/README.md)
