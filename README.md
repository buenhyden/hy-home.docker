# hy-home.docker

> 문서 체계와 모듈형 Docker Compose 구성을 함께 운영하는 홈 인프라 저장소

## Overview

`hy-home.docker`는 홈 서버와 개인 개발 인프라를 Docker Compose 중심으로 표준화하고, 그 위에 요구사항, 설계, 계획, 작업, 운영 지식을 단계별 문서 체계로 연결하는 저장소입니다. 루트 [`docker-compose.yml`](./docker-compose.yml)은 `infra/**/docker-compose*.yml` 파일을 `include`로 통합해 단일 진입점 역할을 수행합니다.

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
- 사용자의 명시적 지시 없이 `docs/01`~`docs/99` 문서를 수정하는 작업

## Structure

```text
hy-home.docker/
├── docs/                 # 00~11, 90, 99 단계 기반 문서 체계
├── infra/                # 계층별 Docker Compose 서비스 정의
├── scripts/              # 사전 점검, 검증, 자동화 스크립트
├── secrets/              # Docker secrets 및 민감 정보 매핑
├── projects/             # 보조 프로젝트 및 예제 작업 공간
├── tests/                # 테스트 관련 문서와 자산
├── docker-compose.yml    # 통합 Compose 진입점
├── .env.example          # 환경 변수 예시
├── AGENTS.md             # Agent 진입 규칙
└── README.md             # 이 문서
```

## Repository Map

- [`docs/`](./docs/) - 요구사항, 아키텍처, 계획, 운영, 사고 대응까지 포함하는 공식 문서 체계
- [`infra/`](./infra/) - `01-gateway`부터 `11-laboratory`까지 계층별 서비스 정의
- [`scripts/`](./scripts/) - 사전 점검, Compose 검증, 하드닝/추적성 검사 스크립트
- [`secrets/`](./secrets/) - Docker secrets 파일 구조와 민감 정보 관리 기준
- [`projects/`](./projects/) - 보조 앱, 스토리북, MCP 관련 프로젝트 공간
- [`.github/workflows/`](./.github/workflows/) - 문서 추적성, 하드닝, pre-commit, 보안 검사를 수행하는 CI 정의

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Orchestration | Docker Compose | 루트 `include` 기반 통합 실행 |
| Infrastructure | 계층형 Compose 스택 | `infra/01`~`infra/11` 서비스 정의 |
| Documentation | Markdown + stage-based docs | `docs/00`~`docs/11`, `docs/90`, `docs/99` |
| Automation | Bash scripts | 사전 점검, 검증, 하드닝, 추적성 검사 |
| CI / Quality | GitHub Actions + pre-commit + zizmor | 문서/보안/품질 게이트 자동화 |

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

`.env`에는 마운트 경로, 네트워크 이름, 서비스별 기본 설정이 포함됩니다. 민감값은 `.env`에 직접 하드코딩하지 말고 [`secrets/`](./secrets/) 구조를 따릅니다.

### 3. 사전 점검 실행

```bash
bash scripts/preflight-compose.sh
```

이 스크립트는 `.env`, 필수 secret 파일, 인증서 파일, 주요 디렉터리, 외부 Docker 네트워크 존재 여부를 점검합니다.

### 4. Compose 구조 검증

```bash
bash scripts/validate-docker-compose.sh
```

이 검증은 누락된 secret 파일을 임시 더미로 보완한 뒤 `docker compose config`가 성공하는지 확인합니다.

### 5. 코어 인프라 실행

```bash
docker compose --profile core up -d
```

기본 코어 계층을 올린 뒤, 필요에 따라 `data`, `obs`, `workflow`, `ai`, `tooling` 같은 프로필을 추가로 활성화할 수 있습니다.

### 6. 주요 진입 문서 확인

1. [`AGENTS.md`](./AGENTS.md) - Agent 작업 진입 규칙
2. [`docs/README.md`](./docs/README.md) - 문서 체계 개요
3. [`docs/00.agent-governance/README.md`](./docs/00.agent-governance/README.md) - 거버넌스 허브
4. [`infra/README.md`](./infra/README.md) - 계층별 인프라 구조
5. [`scripts/README.md`](./scripts/README.md) - 검증 및 자동화 스크립트

## Documentation Standards

이 저장소의 문서는 다음 기준을 따릅니다.

- Agent 전용 규칙 문서는 영어를 사용합니다.
- 사람이 읽는 README, 가이드, 운영 문서는 한국어를 기본으로 사용합니다.
- 문서 작성 작업은 가능한 경우 [`docs/99.templates/`](./docs/99.templates/)의 템플릿을 출발점으로 사용합니다.
- 상위 문서와 하위 산출물 사이의 추적성을 유지하고, 중복된 SSoT 문서를 만들지 않습니다.

## Agent Working Rules

- 작업 시작 전 [`AGENTS.md`](./AGENTS.md)를 먼저 확인합니다.
- Bootstrap 순서는 `bootstrap.md` → `persona.md` → `task-checklists.md` → 해당 scope 순서를 따릅니다.
- 문서 작성/갱신 작업은 [`docs/00.agent-governance/rules/stage-authoring-matrix.md`](./docs/00.agent-governance/rules/stage-authoring-matrix.md)를 기준으로 작성합니다.
- `docs/01`~`docs/99`는 기본적으로 읽기 전용이며, 명시적 사용자 지시가 있을 때만 수정합니다.

## Verification and Quality Gates

로컬 또는 CI에서 자주 사용되는 검증 진입점은 다음과 같습니다.

- `bash scripts/preflight-compose.sh` - 실행 전 필수 파일과 디렉터리 점검
- `bash scripts/validate-docker-compose.sh` - Compose 구조 검증
- `bash scripts/check-doc-traceability.sh` - 문서 추적성 검사
- `bash scripts/check-all-hardening.sh` - 계층별 하드닝 기준 검사
- `pre-commit` - 포맷, 린트, 기본 품질 검사

GitHub Actions에서는 다음 품질 게이트를 사용합니다.

- 문서 추적성 검사
- 템플릿/보안 베이스라인 검사
- QuickWin 베이스라인 검사
- pre-commit 검사
- GitHub Actions 보안 분석 (`zizmor`)

## How to Work in This Area

1. 이 저장소에서 작업을 시작할 때는 먼저 [`AGENTS.md`](./AGENTS.md), [`docs/README.md`](./docs/README.md), [`infra/README.md`](./infra/README.md)를 읽어 전체 구조를 파악합니다.
2. 새 서비스를 추가할 때는 `infra/<tier>/<service>/` 패턴을 따르고, 루트 [`docker-compose.yml`](./docker-compose.yml)의 `include` 및 관련 문서를 함께 검토합니다.
3. 새 문서나 루트 문서를 갱신할 때는 [`docs/99.templates/readme.template.md`](./docs/99.templates/readme.template.md) 같은 승인된 템플릿과 [`docs/00.agent-governance/rules/documentation-protocol.md`](./docs/00.agent-governance/rules/documentation-protocol.md)을 기준으로 삼습니다.
4. 변경 후에는 관련 링크, 검증 명령, 문서 정책, CI 영향 범위를 함께 점검하고 필요한 경우 검증 스크립트를 실행합니다.

## Related References

- [`docs/README.md`](./docs/README.md)
- [`docs/00.agent-governance/README.md`](./docs/00.agent-governance/README.md)
- [`docs/00.agent-governance/scopes/docs.md`](./docs/00.agent-governance/scopes/docs.md)
- [`docs/00.agent-governance/rules/documentation-protocol.md`](./docs/00.agent-governance/rules/documentation-protocol.md)
- [`docs/00.agent-governance/rules/stage-authoring-matrix.md`](./docs/00.agent-governance/rules/stage-authoring-matrix.md)
- [`infra/README.md`](./infra/README.md)
- [`scripts/README.md`](./scripts/README.md)
- [`secrets/README.md`](./secrets/README.md)
