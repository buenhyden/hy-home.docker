---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/harness-engineering.md -->

# Reference: Harness Engineering and Framework Integration

## Overview

본 참조 문서는 AI 에이전트의 개발 환경을 안정적으로 통제하는 하네스 엔지니어링(Harness Engineering)의 기본 설계와 이 워크스페이스에 구현된 3대 LLM(Claude, Codex, Gemini)의 하네스 구축 현황을 조사한 자료입니다.

## Purpose

하네스를 통해 에이전트의 런타임 입력, 도구 바인딩, 그리고 출력 결과를 어떻게 구조화하고 규칙적으로 통제할 수 있는지 살펴봅니다.

## Repository Role

본 문서는 하네스 설계의 참조 정보이며, 실제 런타임 하네스 구성 및 검증 파일(예: `check-repo-contracts.sh`, `validate-harness.sh` 등)의 코드를 대체하지 않습니다.

---

## 1. 하네스 엔지니어링의 정의 및 아키텍처

**하네스 엔지니어링 (Harness Engineering)** 이란 AI 에이전트가 소프트웨어 개발을 안전하고 예측 가능하게 수행할 수 있도록 감싸주는 로컬 실행 테스트베드이자 안전망(Safety Sandbox)을 설계하고 구축하는 공학 활동을 뜻합니다.

- **컨텍스트 유입 통제**: 에이전트가 작업을 시작할 때 불필요한 파일을 읽어 컨텍스트 창(Context Window)을 낭비하지 않도록 JIT(Just-In-Time) 로딩 방식과 특정 디렉토리 구조(Meta-taxonomy)를 제공합니다.
- **도구 및 권한 제약**: 에이전트에게 노출되는 시스템 도구(OS 명령어, 파일 읽기/쓰기 등)의 범위를 지정하고 위험 행동을 격리합니다.
- **자동화된 계약 검증 (Contract Gates)**: 에이전트가 코드를 변경한 뒤, 그 변경 사항이 저장소 계약을 통과했는지 검사하는 로컬 유효성 검증 체계를 제공합니다.

## 2. 3대 LLM(Claude, Codex, Gemini) 하네스 환경 구축 현황

각 인공지능 어시스턴트 툴은 로컬 개발 환경에서 고유한 어댑터와 설정 레이어를 통해 통제되고 있습니다.

### A. Claude Code Harness
- **구조**: `.claude/` 디렉토리를 로컬 런타임 접점으로 사용합니다.
- **에이전트 바인딩**: `.claude/agents/*.md`에 정의된 개별 에이전트 파일이 로컬 실행 시 로드됩니다.
- **훅(Hooks)**: 도구 호출 이후 코드 스타일 정규화 등을 처리할 수 있는 native Claude hook wrapper 체계가 내장되거나 설계되어 있습니다.

### B. Codex Harness
- **구조**: `.codex/` 디렉토리를 사용합니다.
- **에이전트 바인딩**: `.codex/agents/*.toml` 스펙을 통해 도구 권한, 샌드박스 정책, 그리고 세부 프롬프트 지침을 설정합니다.
- **훅(Hooks)**: `.codex/hooks.json`을 사용하여 커밋 전/후 또는 도구 실행 시 디스패치 이벤트를 받아 로컬 검증기를 작동시킵니다.

### C. Gemini Harness
- **구조**: `.agents/` 디렉토리를 런타임 및 지침 어댑터 표면으로 활용합니다.
- **에이전트 바인딩**: `.agents/agents/` 디렉토리와 연계하여 Gemini 고유의 메타데이터 및 지침(instructions)을 주입합니다.
- **특징**: Claude나 Codex처럼 도구 실행 전반을 감시하는 독자적인 런타임 훅 프로세스가 기본 CLI에는 약하므로, 공유 쉘 스크립트(`agent-event-hook.sh`) 및 포스트 검증기(`post-tool-validate.sh`)에 의존하여 Parity(동등성)를 확보합니다.

## 3. 하네스 엔지니어링의 구현 현황 및 부족한 요소

이 워크스페이스에 갖춰진 하네스의 상태와 보완이 필요한 격차를 분석합니다.

- **구현 현황**:
  - `harness-implementation-map.md`를 통해 루트 쉼(Shims), Compose 런타임, 비밀값 규칙, 유효성 검사기, 하드닝, 프로바이더 훅 등이 매우 상세히 매핑되어 있습니다.
  - `validate-harness.sh`와 `check-repo-contracts.sh` 스크립트를 통해 로컬 계약 무결성을 엄격하게 준수하게 만듭니다.
- **부족한 요소 (Gaps)**:
  - **프로바이더별 런타임 격리 수준 편차**: Claude, Codex, Gemini가 사용하는 로컬 샌드박스의 하드닝 수준이 다릅니다. 특히 Gemini 환경의 경우 도구 호출 승인 제어 및 파일 격리가 쉘 수준에 머물러 있어 격리 안전장치 강화가 필요합니다.
  - **문서화 스냅샷의 자동 동기화 지연**: `graphify update` 실행 등이 수동 또는 특정 validator 내부에 결합되어 있어, 에이전트가 작업을 마친 직후 그래프 정보가 실시간으로 자동 갱신되지 못하고 유실될 위험이 존재합니다.

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [loop-engineering.md](./loop-engineering.md)
