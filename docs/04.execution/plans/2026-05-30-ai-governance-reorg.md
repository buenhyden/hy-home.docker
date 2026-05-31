---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-30-ai-governance-reorg.md -->

# AI Agent Governance Reorganization Plan

## Overview (KR)

이 문서는 Antigravity 2.0 IDE, Claude, Codex 에이전트 간의 파편화된 거버넌스(`hy-home.docker`)를 `docs/00.agent-governance/` 기반의 단일 공통 거버넌스(Canonical)로 통합하기 위한 실행 계획 및 기록 문서입니다.

## Context

이 문서는 완료된 2026-05-30 재구성 계획의 역사적 증거로 보존된다. 현재 정책 원천은 `docs/00.agent-governance/`이며, provider surface는 Stage 00 canonical adapter 모델을 따르는 어댑터로 해석한다. 최신 전환 계획과 구현 추적은 2026-06-01 Phase 2/Phase 3 문서를 우선한다.

기존에는 Claude가 Canonical Runtime으로 여겨졌으며 Antigravity(Gemini)와 Codex는 Claude의 구조에 종속적인(단순 미러/포인터) 형태로 관리되었습니다. 이를 개편하여 `docs/00.agent-governance`를 SSOT(Single Source of Truth)로 격상시키고 모든 플랫폼 환경이 어댑터(Adapter) 역할만 하도록 재설계합니다.

## Goals & In-Scope

- **Goals**:
  - `docs/00.agent-governance`를 유일한 원본(Canonical)으로 확립
  - `GEMINI.md` 및 `providers/gemini.md`를 Antigravity 2.0 IDE의 네이티브 규칙(Rules/Skills)을 준수하도록 개편
  - 모델 정책 최신화
  - 파편화된 Hookify 파일 공통화 및 레거시 제거
- **In Scope**:
  - `docs/00.agent-governance/` 하위 문서의 계층 및 정책 갱신
  - `.claude/` 하위 훅 규칙들의 공통화 이동
  - `.agents/` 레거시 디렉토리 삭제

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 기존 Agent들의 동작 코드/스크립트 자체의 구조적 재작성
- **Out of Scope**:
  - Docker 인프라 구성 스크립트 수정

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | 공통 거버넌스 SSOT화 | `providers/agents-md.md`, `subagent-protocol.md` | REQ-GOV-1 | Claude가 원본이라는 문구 제거 확인 |
| PLN-002 | Antigravity 중심 재설계 | `GEMINI.md`, `providers/gemini.md`, `.agents/` | REQ-GOV-2 | 레거시 `.agents/` 제거 및 문서 갱신 확인 |
| PLN-003 | Hookify 제약 공통화 | `.claude/hookify.*.local.md` -> `docs/00.agent-governance/rules/hooks/` | REQ-GOV-3 | 공통 훅 디렉토리로 정상 이동 확인 |
| PLN-004 | 플랫폼 어댑터 패턴 명시 | `providers/claude.md`, `providers/codex.md` | REQ-GOV-4 | 플랫폼별 어댑터 설명 반영 여부 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | 공통 디렉토리에 Hook 파일이 존재하는지 확인 | `ls -la docs/00.agent-governance/rules/hooks/` | Hook 파일들 출력됨 |
| VAL-PLN-002 | Structural | 레거시 .agents 디렉토리가 삭제되었는지 확인 | `ls -d .agents` | 파일이 없다는 오류 출력됨 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 기존 Claude 에이전트들의 훅 참조 실패 | High | `settings.json`이나 훅 스크립트가 템플릿 제약을 위반하지 않도록 사전에 어댑터 스크립트로 동작하게 위임. 향후 플랫폼 훅 파이프라인에서 경로 수정 필요성 확인. |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Operations**: [Operations index](../../05.operations/README.md)
- **Superseding Plan**: [Agent governance Phase 2 alignment plan](./2026-06-01-agent-governance-phase2-alignment.md)
- **Implementation Task**: [Agent governance Phase 3 implementation](../tasks/2026-06-01-agent-governance-phase3-implementation.md)
