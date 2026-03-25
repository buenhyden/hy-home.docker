# hy-home.docker

> **hy-home.docker**: 모듈형 셀프 호스팅 플랫폼 구축을 위한 스펙 중심의 인프라 저장소입니다.

## 1. 개요

이 프로젝트는 Docker 기반의 홈 서버 인프라를 표준화된 환경에서 관리하기 위해 만들어졌습니다. `docs/` 폴더의 문서 체계를 따라 아키텍처 결정(ADR)부터 운영 가이드(Runbook)까지 모든 과정을 명확하게 기록하고 추적하는 것을 목표로 합니다.

## 2. AI 에이전트 가이드

이 저장소는 AI 에이전트가 효율적으로 작업하고 토큰을 절약할 수 있도록 엄격한 관리 원칙을 적용하고 있습니다. 에이전트라면 다음 지침을 반드시 준수해 주세요.

### 1. 정체성과 페르소나 설정

- **시작하기**: 작업을 시작할 때 항상 [AGENTS.md](AGENTS.md)를 먼저 확인하여 전체적인 거버넌스와 규칙을 파악하세요.
- **역할 선택**: [docs/00.agent-governance/rules/persona-matrix.md](docs/00.agent-governance/rules/persona-matrix.md)를 참고해 현재 작업에 가장 적합한 페르소나를 선택하고 해당 규칙을 로드합니다.
- **언어 정책**: 사용자에게 제공하는 모든 응답과 요약은 **한국어**로 작성합니다. 단, `docs/00.agent-governance` 내부의 에이전트 전용 문서나 기술 분석은 효율성을 위해 **영어(English)**를 기본으로 사용합니다.

### 2. 주요 운영 원칙

- **지연 로딩 (Lazy Loading)**: 불필요한 맥락을 미리 읽지 마세요. `[LOAD:RULES:<CAT>]` 마커를 통해 꼭 필요한 규칙만 그때그때 불러와 사용합니다.
- **명세 기반 작업 (Spec-Driven)**: 모든 구현과 수정은 추측이 아닌 `docs/01.prd/` 및 `docs/04.specs/`에 정의된 명세를 근거로 합니다.
- **사전 검증**: 인프라 설정을 변경하기 전에는 반드시 `bash scripts/validate-docker-compose.sh`를 실행해 정합성을 검토하세요.

## 저장소 구조 (Repository Map)

- `docs/` - 표준 문서 체계 (01-11 Taxonomy)
- `infra/` - 인프라 설정 파일 (Docker Compose, Configs)
- `scripts/` - 자동화 및 검증용 쉘 스크립트
- `docs/00.agent-governance/` - AI 에이전트 실행 지침 및 스코프

## 시작하기

1. [AGENTS.md](./AGENTS.md)를 읽고 에이전트의 기본 행동 지침을 확인하세요.
2. [docs/README.md](./docs/README.md)를 통해 문서 관리 방식을 익히세요.
3. 수정 사항이 있다면 [docs/05.plans/](./docs/05.plans/)에 먼저 계획을 작성하고 검토를 받으세요.
