---
status: draft
---
<!-- Target: docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md -->

# Stage 00 AI Agent Governance Standardization Plan

> Use this template for `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.

---

## Overview (KR)

이 문서는 워크스페이스의 **공통 AI Agent 거버넌스(Stage 00)** 와 템플릿 계약, 각 AI Agent(Gemini, Claude, GPT) 플랫폼 하네스의 구조를 워크스페이스 목적에 맞게 재정비하기 위한 실행 계획서다. 2026-05-29 기준 공식 모델 정책, 템플릿 불일치 해소, 중복 규칙 제거, 그리고 플랫폼간(Parity Model) 정합성을 보장하는 것을 목표로 한다.

## Context

- **Workspace Purpose**: Shared harness-engineering and agent-first engineering over modular Docker Compose infrastructure and stage-gated documentation.
- **Current State**:
  - `docs/00.agent-governance/` defines the rules, but platforms have inconsistencies in explicitly mapping the 2026-05-29 state-of-the-art models (`opus-4.8`, `gemini-3.1-pro`, `gpt-5.5`).
  - Template contracts have mismatches (e.g. prompt specifies `policy.template.md` mapping to `docs/05.operations/policies/`, but existing template is `operation.template.md`).
  - `hooks.json` vs `settings.json` hook configurations vary.

## Goals & In-Scope

- **Goals**:
  - Stage 00 거버넌스 개선 및 최신 2026-05-29 공식 모델 정책 반영.
  - Template ↔ 문서 매핑의 1:1 불일치 잔차 제거.
  - 플랫폼별 하네스(Claude, Codex, Gemini) 공통 규범 정렬 및 특화 어댑터 정비.
- **In Scope**:
  - `docs/00.agent-governance/**` 수정 (개념 정의, Model Policy 등).
  - `docs/99.templates/**`와 산출물(docs/01~05) 간의 템플릿 리팩터링 계획.
  - `GEMINI.md`, `CLAUDE.md`, `AGENTS.md` 및 하네스 구조 정비.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 기존 Agent들의 내부 구현 프롬프트 자체를 완전히 새로 짜는 것.
  - 문서 거버넌스와 무관한 서비스/코드 비즈니스 로직 수정.
- **Out of Scope**:
  - 인프라스트럭처 자체의 변경 (Docker Compose 구조 변경 등).

## Target States

### 거버넌스 개선 상태 (Goal State)

1. **Agent / Subagent**: `workflow-supervisor`와 워커 에이전트들의 역할이 명확하며, 모든 런타임이 `docs/00.agent-governance/agents/`를 Canonical로 참고함.
2. **Skill**: `docs/00.agent-governance/agents/functions/`에 단일 정의.
3. **Rule / Hook**: 플랫폼 종속적 Hook 로직은 최소화하고 공통 규칙 `rules/`로 위임.
4. **Output Style**: `rules/output-style.md`가 모든 플랫폼의 기준이 됨.
5. **Memory / QA / CI/CD**: `docs/00.agent-governance/memory/` 기반의 Advisory 메모리 운영.
6. **Model Policy**: 2026-05-29 기준 공식 지원 최신 모델(`opus-4.8`, `sonnet-4.6`, `gpt-5.5`, `gpt-5.5-instant`, `gemini-3.1-pro`, `gemini-3.5-flash`)을 기반으로 명시 및 `reasoning_effort` 정책 확립. 레거시 모델(예: Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro) 사용을 배제하고 최신 환경에 맞게 강제.
7. **Template Contract**: `policy.template.md` 등 1:1 매핑 복구 및 산출물 일치화.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Stage 00 공통 거버넌스 문서 업데이트 | `docs/00.agent-governance/**` | GOV-01 | 중복 규칙 통합, 미확인 모델 보류 처리 |
| PLN-002 | 템플릿 계약 명시 및 매핑 리팩터링 | `docs/99.templates/**`, `docs/01~05` | GOV-02 | 모든 문서가 할당된 템플릿 양식을 준수 |
| PLN-003 | 모델 및 Reasoning 설정 업데이트 | `subagent-protocol.md`, `.claude/settings.json`, `.agents/**` | GOV-03 | 2026-05-29 기준 공식 모델명 적용 |
| PLN-004 | 플랫폼별 하네스 정비 (Claude, Codex, Gemini) | `.claude/**`, `.codex/**`, `.agents/**` | GOV-04 | 공통 거버넌스 기반 어댑터 및 참조 인덱스 정상 동작 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | 템플릿 계약 준수 검증 | `bash scripts/validation/check-repo-contracts.sh` | "PASS: repository Docker/docs contracts are synchronized" |
| VAL-PLN-002 | Structural | Model Policy 검증 | 스크립트 기반 또는 수동 검토 | 모델명이 2026-05-29 기준 공식 모델 목록과 일치함 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 플랫폼 지원 범위를 넘어서는 훅이나 스킬 적용 | Medium | "지원/미지원/보류 항목 목록"을 명확히 문서화하고, 미지원 시 Behavioral Contract로 대체 |
| 과거 문서 포맷 유실 | Low | 템플릿 변환 시 내용(Contents) 보존을 우선시 |

## Completion Criteria

- [ ] Stage 00 공통 거버넌스 업데이트 완료
- [ ] 템플릿 불일치 해소 및 산출물 포맷팅 적용 완료
- [ ] 플랫폼별 하네스 정렬 완료
- [ ] Model & Reasoning Policy 최신화 완료

## Related Documents

- **Task**: [2026-05-30-standardizing-agent-governance task](../tasks/2026-05-30-standardizing-agent-governance.md)
- **Operations**: [Operations index](../../05.operations/README.md)
