---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md -->

# Reference: Multi-Provider Implementation Comparison

## Overview

본 참조 문서는 `hy-home.docker` 워크스페이스 내에서 운용되는 3대 인공지능 어댑터인 Claude Code, Codex, Gemini의 하네스 및 루프 엔지니어링 수준을 대조하고, 공통의 환경 및 규칙 체계를 수립하기 위한 요소를 상세히 비교 분석한 보고서입니다.

## Purpose

프로바이더 간의 동작 방식 차이를 명확히 인지하고, 임의의 프로바이더가 투입되더라도 동등한 안정성을 보장할 수 있는 공통 환경의 설계 방안을 제공합니다.

## Repository Role

본 문서는 멀티 프로바이더 설정 및 특성을 비교하기 위한 분석 자료이며, 실제 개별 프로바이더 설정 파일 및 프로토콜 규약을 수정하지 않습니다.

---

## 1. 3대 프로바이더(Claude, Codex, Gemini) 구현 현황 비교

각 AI 프로바이더가 이 워크스페이스에 통합되어 작동하는 수준을 네 가지 차원으로 분류하여 대조합니다.

| 분류 차원 | Claude Code (Anthropic) | Codex (OpenAI) | Gemini Code Assist (Google) |
| :--- | :--- | :--- | :--- |
| **로컬 어댑터 구조** | `.claude/` 디렉토리에 전용 런타임 설정 보관 | `.codex/` 디렉토리에 TOML 기반 설정 파일 보관 | `.agents/` 디렉토리를 런타임 수용 디렉토리로 구성 |
| **하네스 격리 및 제어** | 로컬 OS 명령 제약 및 특정 워크스페이스 타겟 범위 격리 수준 우수 | 샌드박스 및 명시적 사용자 승인 테이블 관리 정교함 | 쉘 실행 시 실시간 UI 사용자 명시 승인 활용 (로컬 제어 위주) |
| **루프 피드백 (Hooks)** | `agent-event-hook.sh`를 활용한 툴 종료 후 자동 검증 지원 | `.codex/hooks.json` 기반의 정밀 훅 매핑 지원 | 기본 CLI 수준의 훅 바인딩 기능 부재 (수동 실행 또는 상위 래퍼 의존) |
| **에이전트 스펙 형식** | Markdown 형태의 풍부한 지침 정보 활용 | TOML 구조의 기계 파싱이 용이한 설정 활용 | Markdown 파일 및 behavioral pointer 위주 참고 |

## 2. 공통 환경 및 규칙 구축 현황과 과제

현재 이 워크스페이스는 프로바이더별 특징이 다름에도 불구하고, 동일한 거버넌스를 유지하기 위해 **"공통 환경 계약(Common Workspace Contracts)"**을 구축해 두었습니다.

### 공통 규칙 구축 현황
- **Stage 00 중심 거버넌스**: 설정이나 런타임 포맷은 어댑터별로 다를지라도, 에이전트의 역할 정의와 지침은 `docs/00.agent-governance/agents/`에 일괄 정의하고, 린터 및 계약 검증 스크립트(`check-repo-contracts.sh`)가 이를 런타임 폴더로 미러링(Mirroring)하여 동기화합니다.
- **프로바이더 중립적 검증 스크립트**: 모든 린터, 포맷터, 구성 검사기는 특정 LLM에 의존하지 않는 순수 Bash 및 Python 스크립트로 구현되어 있어, 어떠한 에이전트에서도 동일하게 호출 및 재현 가능합니다.

### 부족한 요소 및 개선 방향 (Gaps)
- **비균질적인 훅 연계**: Claude와 Codex는 네이티브 훅 인터페이스를 통해 자동 검증을 루프에 편입시키기 용이하지만, Gemini는 사용자의 명시적 수동 명령어 실행이나 프롬프트 수준의 자발적 유도에 지나치게 기대고 있습니다.
- **프로바이더 능력 편차 대비책 미비**: 추론 성능이나 도구 사용(Tool Use) 방식의 프로바이더 편차로 인해, 특정 에이전트에서는 완벽히 실행되는 워크플로가 타 프로바이더 환경에서는 오동작하거나 비효율적인 루프를 도는 현상이 발생합니다.

## 3. 공통 체계 구축을 위해 보완되어야 할 사항

1. **유니버설 CLI 래퍼(Universal Agent CLI Wrapper)**:
   - 프로바이더 네이티브 도구에 의존하지 않고, 이 워크스페이스의 실행 주기를 직접 통제하는 공통 CLI 래퍼 스크립트를 보완해야 합니다.
   - 이를 통해 Gemini 환경에서도 도구 사용 전/후에 로컬 `post-tool-validate.sh`가 무조건 실행되도록 강제할 수 있습니다.
2. **에이전트 프롬프트 변환 파이프라인 자동화**:
   - `docs/00.agent-governance/`에 작성된 공통 에이전트 스펙(`ci-cd-engineer.md` 등)을 Claude용 `.claude/agents/` 마크다운 양식과 Codex용 `.codex/agents/` TOML 양식으로 빌드 타임에 자동 변환/배포해 주는 파이프라인을 구축해야 합니다.

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
- [ai-agent-catalogs.md](./ai-agent-catalogs.md)
