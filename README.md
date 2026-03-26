# hy-home.docker

> **hy-home.docker**: 홈 인프라를 스펙 기반으로 설계·운영·검증하기 위한 문서 중심 저장소

## 1. 프로젝트 소개

이 저장소는 분산된 홈 서버 구성을 Docker 중심으로 표준화하고, 요구사항부터 운영/사고 대응까지 전 수명주기를 문서 체계로 관리합니다.

핵심 원칙은 다음과 같습니다.

1. 추적성: 요구사항(What/Why)부터 구현/운영 증거까지 연결 가능해야 한다.
2. 검증성: 계획과 작업은 검증 가능한 형태로 기록되어야 한다.
3. 에이전트 협업성: AI Agent가 규칙 기반으로 안정적으로 작업할 수 있어야 한다.

## 2. AI Agent 작업 원칙

### 작업 시작 전 필수

1. [AGENTS.md](./AGENTS.md) 진입 규칙을 먼저 로드한다.
2. [docs/00.agent-governance/rules/bootstrap.md](./docs/00.agent-governance/rules/bootstrap.md)와 [persona.md](./docs/00.agent-governance/rules/persona.md)로 레이어/페르소나를 확정한다.
3. [task-checklists.md](./docs/00.agent-governance/rules/task-checklists.md)의 Pre-Task 체크리스트를 완료한다.
4. 문서 작성/갱신 작업이면 [stage-authoring-matrix.md](./docs/00.agent-governance/rules/stage-authoring-matrix.md)를 기준으로 작성한다.

### 문서 수정 범위 정책

- `docs/00.agent-governance/`와 루트 지시 파일(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)은 에이전트 거버넌스 영역이다.
- `docs/01~99`는 프로젝트 SSoT이며 기본적으로 읽기 전용이다.
- `docs/01~99` 수정은 사용자의 명시적 지시가 있을 때만 수행한다.

## 3. 문서 언어 정책

- AI Agent 작업용 규칙 문서: **영어(English)**
  - 대상: `docs/00.agent-governance/**`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- 사람이 읽는 운영/기획 문서: **한국어(Korean)**
  - 대상: 일반 README, 가이드, 운영/회고 문서 등
- 기본 응답 언어: 사용자와의 상호작용 결과는 한국어를 우선한다.

## 4. 빠른 네비게이션

- 문서 체계 허브: [docs/README.md](./docs/README.md)
- 에이전트 거버넌스 허브: [docs/00.agent-governance/README.md](./docs/00.agent-governance/README.md)
- 통합 체크리스트: [docs/00.agent-governance/rules/task-checklists.md](./docs/00.agent-governance/rules/task-checklists.md)
- 00~11 작성 매트릭스: [docs/00.agent-governance/rules/stage-authoring-matrix.md](./docs/00.agent-governance/rules/stage-authoring-matrix.md)

## 5. 저장소 구조

- `docs/` - 00~11, 90, 99 단계 기반 표준 문서 체계
- `infra/` - Docker Compose 및 서비스별 인프라 설정
- `scripts/` - 검증/자동화 스크립트
- `.agent/` - 로컬 워크플로 및 스킬 자산

## 6. 시작 순서

1. [AGENTS.md](./AGENTS.md) 확인
2. [docs/00.agent-governance/README.md](./docs/00.agent-governance/README.md) 확인
3. 필요한 경우 [docs/05.plans/](./docs/05.plans/)에서 계획 문서 검토 후 작업 시작
