---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md -->

# Reference: AI Agent Catalog and Instruction Audit

## Overview

본 감사는 `hy-home.docker` 워크스페이스 내 AI Agent 지침(Instruction)의 완성도를 평가하고, 외부 대규모 에이전트 카탈로그 `msitarzewski/agency-agents`와의 대조 분석을 통해 식별한 구조적 격차 및 추가 제 제안 에이전트들의 정의서입니다.

## Purpose

에이전트 인스트럭션이 적절히 구조화되어 모호성을 배제하고 있는지 검증하고, 다중 에이전트 오케스트레이션 성능을 극대화할 수 있는 역할 체계를 확보합니다.

## Repository Role

본 문서는 AI 에이전트 카탈로그 설계에 관한 감사 참조 문서이며, 실제 에이전트 규칙 파일이나 런타임에 올라가는 어댑터 파일들을 직접 변경하지 않습니다.

---

## 1. AI Agent Instruction 구조 감사

### A. 구현 현황
- **스코프 분리 준수**: 현재 `docs/00.agent-governance/agents/agents/*.md`에 등록된 15개 에이전트들은 모두 `Purpose`, `Scope (Covers/Excludes)`, `Skills`, `Usage`, `Artifacts`의 형식을 취하고 있으며, 상위 바운더리 스코프(`scopes/agentic.md` 등)를 올바르게 로드하고 있습니다.
- **역할 침범 방지**: `workflow-supervisor`가 다중 도메인 작업을 중앙에서 조율하고 각 하위 worker 에이전트들에게 단일 관심사(Single Responsibility) 중심의 역할을 부여하여 리소스 경쟁 및 무한 루프를 억제합니다.

### B. 격차 및 부족한 요소 (Gaps)
- **인스트럭션 동기화 오차**: 스테이지 게이트 규칙이나 하네스 검증 명령어가 변경될 때, 15개 에이전트 지침 마크다운과 프로바이더 런타임 폴더(`.claude/agents/`, `.codex/agents/` 등)에 투영되는 내용들을 수동 동기화해야 하여, 일부 런타임 지침이 SSOT에서 일시 누락되거나 불일치(Drift)하는 현상이 일어날 우려가 있습니다.

---

## 2. msitarzewski/agency-agents 비교 분석 결과

외부 대규모 MIT 라이브러리인 `agency-agents`와 대조하여, 당 워크스페이스 카탈로그의 보완 방향을 도출합니다.

### A. 카탈로그 규모 및 세분화 격차
- **외부 카탈로그 특징**: `agency-agents`는 140개 이상의 매우 잘게 쪼개진 페르소나(예: CSS Specialist, React Native Expert 등)를 지원하여 문제 해결의 정밀도가 높은 반면, 당 워크스페이스는 `infra-implementer`나 `qa-engineer` 같은 다소 러프한 직군 정의로 인해 복합적인 요구를 한 에이전트가 넓게 처리해야 하는 부담이 있습니다.
- **워크스페이스 개선 기회**: 기업 경영 전반(Marketing, HR 등)의 페르소나는 우리 워크스페이스에 불필요하지만, 개발 품질 강화 및 자동화 가동을 위해 도메인을 특화시킨 3종의 신규 에이전트 도입이 요구됩니다.

---

## 3. 추가 권장하는 3대 AI 에이전트의 상세 설계 명세

워크스페이스 환경에 특화하여 추가로 도입을 권장하는 3종 에이전트의 스펙입니다.

### A. Performance Optimizer (성능 최적화 전문가)
- **목적**: 컨테이너 리소스 오염 및 파일 부하 제어.
- **Scope**:
  - *Covers*: Docker Compose 컨테이너의 메모리/CPU 제한 설정 모니터링, 대량의 지식 디렉토리 스캔 부하 최적화, 스크립트 실행 속도 개선.
  - *Excludes*: 컨테이너 내 비즈니스 로직 자체의 코딩 변경.
- **필요 스킬**: `scripts/validation/run-local-qa-gates.sh --performance` (가상).

### B. Dependency Vulnerability Guardian (의존성 및 취약점 가디언)
- **목적**: 패키지 위협 스캔 및 SBOM 공급망 차단.
- **Scope**:
  - *Covers*: 종속 패키지 스캔 도구(`npm audit` 등) 실행, 오픈소스 라이선스 충돌 감사, CVE 패치 권고 계획 수립.
  - *Excludes*: 실제 운영 인프라의 라이브 자격 증명 갱신.
- **필요 스킬**: `scripts/validation/check-template-security-baseline.sh`.

### C. Prompt/Context Refiner (컨텍스트 정제 에이전트)
- **목적**: JIT 로딩 강제화 및 에이전트 토큰 낭비 제거.
- **Scope**:
  - *Covers*: 컨텍스트 압축, 불필요한 히스토리 및 중간 로그의 요약 필터링, 프롬프트 최적화 지침 가이드.
  - *Excludes*: 마크다운 이외의 빌드 코드 생성.
- **필요 스킬**: `caveman` (지식 압축 스킬 활용).

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [harness-loop-audit.md](./harness-loop-audit.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
- [../../research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md](../../research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md)
