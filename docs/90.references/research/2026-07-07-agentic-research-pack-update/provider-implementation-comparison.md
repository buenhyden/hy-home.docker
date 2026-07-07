---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md -->

# Reference: Multi-Provider Implementation Comparison

본 문서는 `hy-home.docker` 워크스페이스 내에서 운용되는 3대 주요 AI Provider(Claude Code, OpenAI Codex, Gemini Code Assist)의 하네스 엔지니어링과 루프 엔지니어링 구현 깊이를 구체적으로 비교 분석하고, 공통의 환경 및 규칙 체계를 수립하기 위한 기술적 대안과 런타임 어댑터 아키텍처를 연구한 레퍼런스 자료입니다.

---

## 목차 (Table of Contents)

1. [3대 AI Provider의 런타임 비교 아키텍처](#1-3대-ai-provider의-런타임-비교-아키텍처)
2. [하네스 및 루프 엔지니어링 상세 비교 매트릭스](#2-하네스-및-루프-엔지니어링-상세-비교-매트릭스)
3. [공통의 규칙 및 환경 구축을 위한 아키텍처 제안](#3-공통의-규칙-및-환경-구축을-위한-아키텍처-제안)
4. [결론 및 차기 개선 기회 (Gaps)](#4-결론-및-차기-개선-기회-gaps)

---

## 1. 3대 AI Provider의 런타임 비교 아키텍처

AI 에이전트 런타임은 각각의 고유한 시스템 설계 철학을 가집니다. 따라서 로컬 워크스페이스 내에 이식되는 디렉토리 레이아웃, 설정 형식, 그리고 훅 결합 방식 역시 큰 차이를 보입니다.

*   **Claude Code (`.claude/`)**: 마크다운 기반의 시스템 프로토콜과 프롬프트를 직관적으로 처리하는 데 강점을 둡니다. 에이전트 본문이 Stage 00 마크다운 지침과 직접 호환되며, 파일 편집이나 명령어 실행 이후 가동되는 쉘 스크립트 기반의 훅 연동이 매우 기밀하게 결합되어 있어 리얼타임 유효성 검증 성능이 가장 뛰어납니다.
*   **OpenAI Codex (`.codex/`)**: 정교한 기계적 제어와 명세 중심의 규제를 지향합니다. TOML 환경설정 포맷을 활용하여 도구의 화이트리스트 접근 경로와 실행 파라미터 제약조건을 고도로 한정하며, 샌드박스의 논리 격리 강도가 가장 높아 안전성 면에서 신뢰할 수 있습니다.
*   **Gemini Code Assist (`.agents/`)**: 구글 워크스페이스 및 IDE와의 네이티브 연동을 우선으로 설계되었습니다. 프로토콜 파일이 로컬 터미널이나 에이전트 런타임 프로세스에 의해 직접 가로채어 실행되기 어려운 구조를 취하고 있어, 로컬 훅에 의한 동적 감시보다는 프롬프트 기반의 자율 규제에 상당 부분을 할당합니다.

---

## 2. 하네스 및 루프 엔지니어링 상세 비교 매트릭스

3대 Provider의 핵심 설계 요소를 하네스 격리도, 피드백 루프 완성도, 규칙 준수 신뢰성 관점에서 대조 평가한 표입니다.

| 평가 차원 및 지표 | Claude Code | OpenAI Codex | Gemini Code Assist |
| :--- | :--- | :--- | :--- |
| **물리 파일 레이아웃** | `.claude/settings.json`<br>`.claude/agents/*.md` | `.codex/settings.toml`<br>`.codex/agents/*.toml` | `.agents/settings.json`<br>`.agents/agents/*.md` |
| **설정 및 명세 형식** | Markdown + JSON | TOML + JSON Schema | Markdown + JSON |
| **도구 권한 격리 수준 (Sandbox)** | 상 (CLI 키보드 Y/N 프롬프트 결합) | 최상 (TOML 화이트리스트 물리 격리) | 중 (IDE 호스트 OS 실행 권한 종속) |
| **런타임 훅 지원 (Hooking)** | 최상 (Post-tool, Pre-run 네이티브 지원) | 상 (Hooks.json 매핑 기반 동적 가로채기) | 하 (네이티브 훅 결여, 수동 확인 의존) |
| **오류 피드백 루프 (Loop Parity)** | 최상 (에러 로그를 Context에 즉각 피딩) | 상 (동적 검증 실패를 JSON으로 변환) | 중 (사용자 프롬프트 수동 재주입 필요) |
| **DORA 연계 리드타임 감축력** | 상 (로컬 훅 즉시 보정으로 PR 빌드 패스율 극대화) | 중상 (계약 위반 조기 탐지) | 중 (원격 CI 빌드 도달 후 에러 교정) |
| **규칙 수렴도 (Self-Correction)** | 상 (Thought-Act 순환 내에서 규칙 자동 수렴) | 중상 (명세 위반 시 동작 거부 위주) | 중 (자율 프롬프트 이해 수준에 편차 존재) |

---

## 3. 공통의 규칙 및 환경 구축을 위한 아키텍처 제안

Provider 간의 고유 격차(Gemini의 훅 결여, Codex의 TOML 고집 등)로 인해 발생하는 거버넌스 파편화를 제어하려면, **Stage 00 에이전트 스펙 컴파일러**와 **공통 도구 실행 래퍼**의 구축이 필수적입니다.

```text
       Stage 00 SSoT Agent Specs (Markdown)
                       │
                       ▼
      [check-repo-contracts.sh (Compiler)]
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
  Claude Adapter  Codex Adapter  Gemini Adapter
  (.claude/*.md)  (.codex/*.toml) (.agents/*.md)
```

### 3.1 에이전트 스펙 컴파일러 (Spec Compiler)
본 워크스페이스는 모든 규칙을 마크다운 형태의 `docs/00.agent-governance/agents/` 디렉토리에 하나의 원천 소스(SSoT)로 관리합니다.
`check-repo-contracts.sh` 스크립트는 이 마크다운 명세들을 읽어 다음과 같은 형식으로 각각의 Provider 어댑터에 100% 동기화 투영(Projections)합니다.
-   **Claude Projection**: 마크다운 헤더 구조를 보존하여 `.claude/agents/*.md` 파일로 복사.
-   **Codex Projection**: 마크다운 내의 도구 스펙과 제외 스코프를 파싱하여 `.codex/agents/*.toml` 파일의 TOML 화이트리스트 노드로 자동 번역.
-   **Gemini Projection**: IDE 컨텍스트 인덱스를 위한 참조 주소로 `.agents/agents/*.md`로 파싱 전송.

### 3.2 공통 도구 실행 래퍼 (Shared Tool Wrapper)
-   에이전트가 런타임 호스트의 파일과 인프라에 접근할 때 네이티브 바이너리(`git`, `docker`)를 직접 부르지 않고, 반드시 `scripts/hooks/post-tool-validate.sh` 및 `validate-harness.sh`를 포함하는 공통 쉘 래퍼를 경유하도록 에이전트 시스템 지침에 선언합니다.
-   이 래퍼는 에이전트가 작성한 파일을 즉각적이고 무조건적으로 `git diff --check` 및 `prettier --check`로 정방향 교정한 후, 최종 성공 코드(Exit Code 0)만 에이전트의 런타임에 전달하는 방식으로 Gemini 등의 훅 차이를 평탄화(Flat Mapping)합니다.

---

## 4. 결론 및 차기 개선 기회 (Gaps)

### 4.1 요약
Provider별 특성 차이는 제거할 수 없는 벤더 고유의 한계이지만, 워크스페이스 수준의 컴파일러와 통합 래퍼를 견고히 구축함으로써 에이전트에게 공급되는 거버넌스 규칙과 품질 게이트의 균일성(Unified Enforcement)을 안정적으로 획득할 수 있습니다.

### 4.2 부족한 요소 (Gaps)
1.  **동적 어댑터 템플릿의 자동 제어 부재**: 현재 `check-repo-contracts.sh`는 어댑터들의 Parity 상태를 단방향으로 검증할 뿐, 누락된 어댑터 파일을 Stage 00 원본으로부터 자동으로 빌드 및 작성하는 생성(Scaffolding) 기능이 미흡합니다. 이를 보강하여 생성-동기화가 하나의 컴파일러 명령어로 동작하도록 구현해야 합니다.
2.  **공통 Context 용량 제어 부족**: Claude에 특화된 프롬프트 지침이 Gemini로 그대로 주입될 때 컨텍스트 오버헤드를 유발합니다. Provider별로 허용된 컨텍스트 제한을 인식하여 마크다운 본문의 상세도를 동적으로 Pruning하는 Context Refiner 모듈이 추가로 요구됩니다.

---

## Sources

- [Provider Capability Matrix](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/rules/provider-capability-matrix.md) - 주요 벤더별 기능 및 제한 SSoT
- [Subagent Protocol Model Policy](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/subagent-protocol.md) - 에이전트 등급 및 할당 매트릭스
- [Claude CLI Specification](https://code.claude.com/docs/en/overview) - Claude CLI 아키텍처
- [Codex Hook Event Schema](https://developers.openai.com/codex/hooks) - Codex 실행 게이트 스키마

---

## Maintenance

- **소유자**: 워크스페이스 아키텍처 및 거버넌스 수석 아키텍트
- **검토 주기**: 연 1회 혹은 신규 AI 어댑터 스펙 릴리스 시
- **업데이트 트리거**: `check-repo-contracts.sh` 린트 알고리즘 개정 및 신규 모델 할당 정책 변경 시
