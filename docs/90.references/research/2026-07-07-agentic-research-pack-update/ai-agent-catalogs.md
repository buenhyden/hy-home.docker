---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Comparative Persona Analysis

## Overview

본 참조 문서는 외부 대규모 AI 에이전트 카탈로그 라이브러리인 `msitarzewski/agency-agents`와 `hy-home.docker` 워크스페이스 내에 구축된 15대 전용 에이전트 체계를 대조 분석하고, 워크스페이스 내 AI Agent 지침(Instructions) 구조 및 추가 도입 가능한 에이전트 정의를 제안한 연구 보고서입니다.

## Purpose

에이전트 역할 세분화 수준을 평가하고, 당 워크스페이스의 특성에 부합하는 전문 에이전트 추가 기회를 포착합니다.

## Repository Role

본 문서는 에이전트 카탈로그 아키텍처 비교를 위한 참조용 레퍼런스이며, 실제 에이전트 카탈로그 파일이나 모델 실행 프로토콜을 변경하지 않습니다.

---

## 1. AI Agent Instruction 구조 및 설계 원칙

이 워크스페이스에 구현된 AI Agent 지침(Instruction) 마크다운은 다음과 같은 명확한 계층구조 표준을 따릅니다.

- **Overview / Purpose**: 해당 에이전트의 목표와 존재 목적 명시.
- **Scope (Covers & Excludes)**: 에이전트가 처리할 수 있는 도메인 영역과, 다른 에이전트에게 위임해야 할 영역을 명시적으로 구분하여 역할 침범 방지.
- **Structure**: 참조하는 상위 바운더리 스코프(`meta.md`, `docs.md` 등)와 프로바이더 권장 모델 티어 지정.
- **Skills & Functions**: 해당 에이전트가 다룰 수 있는 전용 스킬 파일(`functions/*.md`)의 링크 제공.
- **Usage & Artifacts**: 에이전트 트리거 요건과, 실행 후 반드시 남겨야 할 산출물 정의.

## 2. msitarzewski/agency-agents vs hy-home.docker 비교 분석

두 카탈로그 모델의 철학과 구조적 차이를 정리합니다.

| 비교 차원 | msitarzewski/agency-agents | hy-home.docker Curated Catalog |
| :--- | :--- | :--- |
| **목적 및 방향성** | 140개 이상의 대규모 범용 에이전트 페르소나 라이브러리 | 저장소 인프라와 SDLC에 특화된 15개 에이전트 팀 |
| **조직적 분류** | 16대 기업 조직부서(Engineering, Product, Marketing 등) 기반 | 가상 엔지니어링 수행을 위한 작업자 직군 기반 |
| **도구 및 권한 연계** | 개별 도구(Claude Code, Cursor 등) 설치 스크립트 제공 위주 | 하네스 맵 및 계약 검증 스크립트와 완전히 결합됨 |
| **역할 격리 방식** | 페르소나와 작업 시나리오 중심 서술 | 스코프(Covers/Excludes)를 통한 기능 경계 제어 |

### 워크스페이스 구현 에이전트 현황 (15대 에이전트)
1. `workflow-supervisor`: 전체 작업 조율 및 최종 합성.
2. `ci-cd-engineer`: 빌드 파이프라인 및 배포 파이프라인 전담.
3. `code-reviewer`: 정적 분석 및 PR 코드 무결성 검사.
4. `doc-writer`: 설계서 및 운영 문서 작성.
5. `drift-detector`: 인프라 구성 드리프트 및 버저닝 추적.
6. `hook-developer`: 프로바이더 훅 및 자동화 래퍼 작성.
7. `iac-reviewer`: Docker Compose 및 인프라 명세 검토.
8. `incident-responder`: 사고 해결 및 로깅, 런북 가이드 관리.
9. `infra-implementer`: 실제 인프라 설치 및 네트워킹 설정.
10. `qa-engineer`: 테스트 케이스 정의 및 로컬 검증 실행.
11. `rules-engineer`: 거버넌스 규칙 및 가이드라인 제어.
12. `security-auditor`: 비밀값 누출 검사 및 취약점 진단.
13. `skill-creator`: 신규 스킬 파일 및 유틸리티 개발.
14. `style-enforcer`: 마크다운 및 코드 포맷 정규화.
15. `wiki-curator`: LLM Wiki 지식 맵 관리.

## 3. 외부 카탈로그 대비 누락 요소 및 보완 사항

- **세분화된 도메인 엔지니어(Domain-specific Engineers) 부족**: `agency-agents`에는 Frontend Developer, Backend Developer, Database Administrator 등 기능 단위 도메인 에이전트가 존재하나, 당 워크스페이스는 `infra-implementer`와 `qa-engineer` 같이 비교적 포괄적인 직군으로 정의되어 있습니다.
- **시나리오 기반 가이드라인 부족**: `agency-agents`는 에이전트가 실제 상황(예: 데이터베이스 마이그레이션 실패, 프론트엔드 CSS 레이아웃 깨짐 등)에서 취해야 하는 상호작용 지침이 정밀하나, 당 워크스페이스의 지침은 입출력 구조 정의에 집중되어 있습니다.

## 4. 추가 제안하는 AI Agents 및 상세 내용

본 워크스페이스의 품질 향상 및 인프라 통제를 위해 추가 도입을 제안하는 3종의 전용 에이전트 명세입니다.

### A. Performance Optimizer (성능 최적화 전문가)
- **목적**: 인프라 리소스 소모량 감시 및 어플리케이션 병목 진단.
- **주요 임무**: Docker Compose 리소스 제한(`limits`), 대용량 마크다운 렌더링 부하 분석, 데이터베이스 인덱스 제안.
- **필요한 스킬**: `docker-resource-profiling`, `performance-regression-audit`.

### B. Dependency Vulnerability Guardian (의존성 및 취약점 가디언)
- **목적**: SBOM 생성 상태 감시 및 패키지 보안 위협 차단.
- **주요 임무**: `npm audit` 등 종속성 도구 자동 실행, 컨테이너 베이스 이미지 취약점(CVE) 스캔 보고서 해석.
- **필요한 스킬**: `dependency-scanner`, `cve-severity-classifier`.

### C. Prompt/Context Refiner (컨텍스트 정제 에이전트)
- **목적**: 에이전트 호출 시점의 컨텍스트 창 최적화 및 낭비 차단.
- **주요 임무**: 사용하지 않는 히스토리 트리 컷오프, 대용량 파일 요약본 치환, 헬퍼 프롬프트 작성.
- **필요한 스킬**: `context-window-pruning`, `instruction-compressor` (예: `caveman` 스킬 활용).

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [provider-implementation-comparison.md](./provider-implementation-comparison.md)
- [../../../../00.agent-governance/agents/README.md](../../../00.agent-governance/agents/README.md)
