---
title: "hy-home.docker"
version: "1.3.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# hy-home.docker

> 모듈형 Docker Compose 홈 인프라를 위한 shared harness-engineering and agent-first engineering workspace.

## Overview

`hy-home.docker`는 shared harness-engineering and agent-first engineering workspace 저장소입니다. 홈 서버와 개인 개발 인프라를 Docker Compose 중심으로 표준화하고 그 위에 요구사항, 설계, 계획, 작업, 운영 지식을 단계별 문서 체계로 연결합니다. 루트 [`docker-compose.yml`](./docker-compose.yml)은 Git으로 추적하는 `infra/**/{compose,docker-compose}*.{yml,yaml}` 파일을 `include`로 통합해 단일 진입점 역할을 합니다.

이 저장소의 핵심 목적은 세 가지입니다. 인프라 구성을 계층별로 분리해 서비스 추가와 변경 영향을 명확히 하고 문서와 실행 대상을 연결해 추적성과 검증 가능성을 확보합니다. 여기에 AI Agent와 사람이 동일한 규칙 아래에서 안전하게 협업할 수 있도록 진입 규칙과 작업 범위를 명확히 유지합니다.

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
├── .agents/              # 공통 Agent 거버넌스, 역할, 호출 절차
├── docs/                 # 01~05, 90, 98, 99 공식 문서 체계
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

- [`docs/`](./docs/README.md) - 요구사항, 아키텍처, 명세, 실행, 운영 지식까지 포함하는 공식 문서 체계
- `docs/05.operations` - 사용 가이드, 운영 정책, 런북, 사고 기록을 분리해 관리하는 운영 지식 베이스
- `docs/90.references` - Docker, 학습 로드맵 등 느리게 변하는 참고 지식
- [`llms.txt`](./llms.txt) - LLM 에이전트용 repo-local 탐색 진입점
- [`infra/`](./infra) - `01-gateway`부터 `11-laboratory`까지 계층별 서비스 정의
- [`scripts/`](./scripts) - 사전 점검, Compose 검증, 하드닝/추적성 검사 스크립트
- [`secrets/`](./secrets) - Docker secrets 파일 구조와 민감 정보 관리 기준
- [`projects/`](./projects) - 보조 앱, 스토리북, MCP 관련 프로젝트 공간
- [`.github/workflows/ci-quality.yml`](.github/workflows/ci-quality.yml) - repository contract, Git flow, Compose, 하드닝, pre-commit, 보안 검사를 수행하는 CI 정의
- `docs/90.references/data` - Docker image/version drift의 관찰 시점이 명시된 참고 자료
- `docs/98.archive/completed/03.specs/0095-infra-secrets-docs-refresh` - infra, secrets, 운영 문서 최신화 분석 명세

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Orchestration | Docker Compose | 루트 `include` 기반 통합 실행 |
| Infrastructure | 계층형 Compose 스택 | `infra/01`~`infra/11` 서비스 정의 |
| Documentation | Markdown + stage-based docs | `docs/01`~`docs/05`, `docs/90`, `docs/98`, `docs/99` |
| Automation | Bash scripts | 사전 점검, 검증, 하드닝, 추적성 검사 |
| CI / Quality | GitHub Actions + pre-commit + zizmor | 문서/보안/품질 게이트 자동화 |
| Version Drift Gate | [`infra/tech-stack.versions.json`](./infra/tech-stack.versions.json) | Compose image 선언에서 파생한 기계 판독 projection의 drift 검사. 런타임 pin 원본은 Compose/Dockerfile 선언 |

## Current Infrastructure Snapshot

인프라 규모는 문서 상수로 고정하지 않고, 항상 아래 명령과 소유 문서에서 재현합니다.

- Compose 파일 수와 root `include` 수: `git ls-files 'infra/**/*compose*.yml' 'infra/**/*compose*.yaml'`
- 활성화되는 서비스 목록과 HOME/DEV/OPTIONAL/LAB/MIGRATE 분류 근거: [`infra/README.md`](./infra/README.md)의 Compose Inventory Snapshot
- 루트 `docker-compose.yml`의 secret 선언과 등록된 secret file path: [`secrets/README.md`](./secrets/README.md)
- tracked README 파일 수: `git ls-files '*README.md' | wc -l`
- README 최신화 기준: `docs/99.templates/templates/common/readme-repository.template.md`의 공통 구조와 경로별 snippet

위 항목의 모든 수치는 추적 트리와 명령 실행에서 재현할 수 있어야 합니다. `secrets/`의 값과 인증서 파일은 추적 대상이 아니므로 개수를 기록하지 않습니다. 추적되지 않는 로컬 상태는 저장소가 재현할 수 없고, 기록하면 검증 없이 낡습니다.

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

기본 검증은 선언된 각 profile과 POL-0078의 HOME named selection을 각각 렌더링하여 `docker compose config`가 성공하는지, resolved service count가 0이 아닌지, 그리고 각 선택이 공개하는 host port가 충돌하지 않는지 확인합니다. 따라서 HOME 조합에서만 드러나는 profile 간 port 충돌도 검사합니다. `HYHOME_COMPOSE_PROFILES="core dev"`처럼 지정하면 그 조합 하나만 검증합니다. profile 선언은 Compose 구성에서 확인하고, 운영 문서는 [문서 인덱스](docs/README.md)에서 탐색합니다. POL-0078의 HOME selection은 검증 스크립트가 조합 검사에 필요한 machine section만 읽는 입력이며 agent 실행 규칙을 소유하지 않습니다. 검증 스크립트는 누락된 로컬 `.env` 또는 dummy secret 파일을 임시로 만들 수 있으므로, evidence에는 검증 profile과 임시 파일 cleanup 여부를 함께 기록합니다.

### 5. Repository contract 검증

```bash
python3 scripts/validation/run-ci-gate.py --profile full
```

이 검증은 docs taxonomy, required README, template inventory, GitHub Actions YAML, duplicate workflow step, script reference, runtime agent/function catalog, Docker image tag policy, tech-stack version drift를 함께 확인합니다.

### 6. 코어 bootstrap과 HOME 선택

```bash
docker compose --profile core up -d
```

`core`는 bootstrap selection일 뿐 HOME 전체가 아닙니다. 현재 HOME 후보는
`core mng ai workflow storage obs-core obs-host availability logs alerting
tracing profiling obs-gpu registry`의 명시적 결합이며, 선택되는 정확한 서비스 수는
`COMPOSE_PROFILES=core,mng,ai,workflow,storage,obs-core,obs-host,availability,logs,alerting,tracing,profiling,obs-gpu,registry docker compose --env-file .env.example config --services`로
재현합니다. 이 명령은 배포 승인이나 용량·복구 증명이 아닙니다. profile 어휘, 구성원, 제외 규칙은
[문서 인덱스](./docs/README.md)의 Compose Profile Vocabulary Policy
(POL-0078)가 소유합니다. Canonical path는
`docs/05.operations/policies/0078-compose-profile-vocabulary.md`입니다. `tooling`은 SonarQube(registry는 HOME의 `registry` profile), `testing`은 k6와 Locust,
`iac`은 OpenTofu와 Terrakube의 명시적 운영 작업에만 사용합니다. Renovate는
`dependency-update` 전용 job이며 `tooling`이나 HOME 선택에 포함되지 않습니다.

### 7. 주요 진입 문서 확인

1. [`AGENTS.md`](./AGENTS.md) - Agent 작업 진입 규칙
2. [`docs/README.md`](./docs/README.md) - 문서 체계 개요
3. [`.agents/README.md`](.agents/README.md) - 거버넌스 허브
4. [`infra/README.md`](./infra/README.md) - 계층별 인프라 구조
5. [`scripts/README.md`](./scripts/README.md) - 검증 및 자동화 스크립트
6. [`llms.txt`](./llms.txt) - LLM 에이전트용 repo-local 탐색 진입점

## Documentation Standards

이 저장소의 문서는 다음 기준을 따릅니다.

- 문서 작성 작업은 가능한 경우 `docs/99.templates`의 템플릿을 출발점으로 사용합니다.
- 상위 문서와 하위 산출물 사이의 추적성을 유지하고, 중복된 SSoT 문서를 만들지 않습니다.

문서 언어는 [문서 언어 규칙](.agents/governance/documentation-protocol.md#document-language)이 정합니다.

## Documentation Lifecycle

문서 stage는 역할이 겹치지 않도록 다음 흐름으로 관리합니다.

| Stage | Responsibility |
| --- | --- |
| `docs/01.requirements` | 사용자 가치, 문제 정의, 요구사항, 성공 기준 |
| `docs/02.architecture` | 아키텍처 요구사항과 결정 기록 |
| `docs/03.specs` | 기능별 기술 명세, 인터페이스, 구현 계약과 co-located Plan/Task evidence |
| `docs/05.operations` | 운영 가이드, 정책, 런북, 사고 기록 |
| `docs/90.references` | 느리게 변하는 참고 지식, 용어, source-backed reference |
| `docs/99.templates` | 새 문서와 README의 canonical template |

일반 작업 흐름은 요구사항 → 아키텍처 → 명세 → 실행 → 운영 순서입니다. 참고 문서는 active stage를 대체하지 않고, 템플릿은 새 문서 작성 전에 target 위치와 상대 링크를 다시 계산하는 기준으로만 사용합니다.

## Common Documentation Workflows

| Workflow | Start Here | Then Update | Verify |
| --- | --- | --- | --- |
| 새 요구사항 정의 | `docs/01.requirements/README.md` | PRD → ARD/ADR → Spec 링크를 target-relative로 연결 | `python3 scripts/validation/run-ci-gate.py --profile changed` |
| 아키텍처 선택 기록 | `docs/02.architecture/README.md` | ARD 또는 ADR, 관련 Spec 링크 | `python3 scripts/validation/run-ci-gate.py --profile changed` |
| 구현 명세 작성 | `docs/03.specs/README.md` | Spec child contracts and execution plan links | `python3 scripts/validation/run-ci-gate.py --profile changed` |
| 실행 계획/작업 evidence 갱신 | `docs/03.specs/README.md` | owning capability에 Plan과 Task를 co-locate하고 검증 evidence 기록 | `python3 scripts/validation/check-document-links.py --mode traceability` |
| 운영 지식 갱신 | `docs/05.operations/README.md` | guide, policy, runbook, incident 목적별 배치 | `python3 scripts/validation/run-ci-gate.py --profile changed` |
| 참고 지식 추가 | `docs/90.references/README.md` | Reference가 active policy나 runbook을 대체하지 않는지 확인 | `python3 scripts/validation/run-ci-gate.py --profile changed` |
| 템플릿 변경 | `docs/99.templates/README.md` | Template-to-folder mapping and target-relative links | `python3 scripts/validation/run-ci-gate.py --profile changed` |

새 문서 작업은 항상 해당 stage README에서 시작하고, 생성된 문서의 `## Related Documents` 링크는 템플릿 파일 위치가 아니라 복사된 target 문서 위치 기준으로 다시 계산합니다.

## Agent Working Rules

- 작업 시작 전 [`AGENTS.md`](./AGENTS.md)를 먼저 확인합니다.
- Bootstrap 순서는 [canonical bootstrap](.agents/governance/bootstrap.md#canonical-load-order)이 소유합니다. Root shim을 통해 해당 native provider 문서와 필요한 정책·역할·명시적으로 선택한 skill, 현재 Spec/Task를 읽습니다.
- 문서 작성/갱신 작업은 [`.agents/governance/stage-authoring-matrix.md`](.agents/governance/stage-authoring-matrix.md)를 기준으로 작성합니다.
- 공식 stage 문서는 기본적으로 읽기 전용이며, 명시적 사용자 지시가 있을 때만 수정합니다.

## Verification and Quality Gates

로컬 또는 CI에서 자주 사용되는 검증 진입점은 다음과 같습니다.

- `bash scripts/validation/validate-docker-compose.sh --preflight` - 실행 전 필수 파일과 디렉터리 점검
- `python3 scripts/validation/run-ci-gate.py --profile changed` - 변경 경로가 영향을 주는 public suite 실행
- `python3 scripts/validation/run-ci-gate.py --profile full` - six public validation suites 전체 검증
- `bash scripts/validation/validate-docker-compose.sh` - profile-aware Compose 구조 검증
- `python3 scripts/validation/check-document-links.py --mode traceability` - 문서 추적성 검사
- `python3 scripts/validation/check-document-links.py --mode alignment` - 문서 링크·anchor·archive 경계·폐기 템플릿 검사
- `bash scripts/validation/check-quickwin-baseline.sh` - QuickWin baseline 검사
- `bash scripts/validation/check-template-security-baseline.sh` - 템플릿 채택 및 필수 보안 baseline 검사
- `bash scripts/hardening/check-all-hardening.sh` - 계층별 하드닝 기준 검사

`pre-commit`은 CI와 hook 정책에서 관리하며, 이 저장소 지시가 바뀌지 않는 한 수동 실행을 기본 절차로 두지 않습니다.

GitHub Actions 품질 게이트는 PR에서 `validation-changed`, push와 manual
dispatch에서 `validation-full`을 사용합니다. 두 job은 각각 public
`changed` 또는 `full` profile만 선택하며 validator 명령을 복사하지 않습니다.

추가로 `v*.*.*` 태그 push에는 `Release Changelog Check`가 실행되어
`CHANGELOG.md`에 해당 release tag 항목이 있는지 확인합니다. 이는 tag-only
release visibility gate이며, remote required-check enforcement 증거로
간주하지 않습니다.

`validation-full` job은 GitHub Actions 보안 분석 결과를 SARIF로 산출합니다. `stale`, `greetings`,
`pr-labeler` workflow는 triage/community 자동화이며 필수 품질 게이트에는 들지 않습니다.
로컬에서는 `python3 scripts/validation/run-ci-gate.py --profile changed --explain`으로
선택된 suite와 validator 매핑을 실행 없이 확인합니다.

Workflow의 외부 `uses:`는 full commit SHA로 고정하고, 직접 작성한 action step에는 명시적 `name`을 둡니다.

## Usage

1. 이 저장소에서 작업을 시작할 때는 먼저 [`AGENTS.md`](./AGENTS.md), [`docs/README.md`](./docs/README.md), [`infra/README.md`](./infra/README.md)를 읽어 전체 구조를 파악합니다.
2. 새 서비스를 추가할 때는 `infra/<tier>/<service>/` 패턴을 따르고, 루트 [`docker-compose.yml`](./docker-compose.yml)의 `include` 및 관련 문서를 함께 검토합니다.
3. 새 문서나 루트 문서를 갱신할 때는 `docs/99.templates/templates/common/readme-repository.template.md` 같은 승인된 템플릿과 [`.agents/governance/documentation-protocol.md`](.agents/governance/documentation-protocol.md)을 기준으로 삼습니다.
4. Docker image runtime pin을 바꿀 때는 해당 Compose/Dockerfile 선언을 먼저 바꾸고, [`infra/tech-stack.versions.json`](./infra/tech-stack.versions.json) 파생 projection과 동기화 검사를 함께 점검합니다. Dockerfile `FROM`/`ARG` pin은 Compose image projection과 별도 authority입니다.
5. GitHub workflow를 바꿀 때는 [`.agents/governance/github-governance.md`](.agents/governance/github-governance.md)와 [`.agents/governance/git-workflow.md`](.agents/governance/git-workflow.md)를 기준으로 branch, permission, SHA pinning, step naming을 확인합니다.
6. 변경 후에는 관련 링크, 검증 명령, 문서 정책, CI 영향 범위를 함께 점검하고 필요한 경우 검증 스크립트를 실행합니다.

## Related Documents

- [`docs/README.md`](./docs/README.md)
- [`.agents/README.md`](.agents/README.md)
- [`.agents/governance/documentation-protocol.md`](.agents/governance/documentation-protocol.md)
- [`.agents/governance/github-governance.md`](.agents/governance/github-governance.md)
- [`.agents/governance/git-workflow.md`](.agents/governance/git-workflow.md)
- [`.agents/governance/stage-authoring-matrix.md`](.agents/governance/stage-authoring-matrix.md)
- `docs/05.operations/README.md`
- `docs/90.references/README.md`
- `docs/90.references/data/README.md`
- [`llms.txt`](./llms.txt)
- `docs/98.archive/completed/03.specs/0095-infra-secrets-docs-refresh/spec.md`
- Historical execution evidence: `plan-0028` (retained through the typed change ledger)
- [`infra/README.md`](./infra/README.md)
- [`infra/tech-stack.versions.json`](./infra/tech-stack.versions.json)
- [`scripts/README.md`](./scripts/README.md)
- [`secrets/README.md`](./secrets/README.md)
