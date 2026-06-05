---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-26-workspace-audit-gap-closure.md -->

# Workspace Audit Gap Closure Plan

## Overview

이 문서는 2026-05-26 워크스페이스 감사(2차 세션)의 실행 계획서다. 이전 감사 세션(`2026-05-26-workspace-audit.md`)에서 식별된 신규 갭(GAP-NEW-03~10)을 클로저하기 위한 저위험 변경 목록, 검증 기준, 지연 항목을 정의한다.

## Context

첫 번째 감사 세션에서 18개 스킬, env/secrets 비교, stage README 보강을 완료한 후, 두 번째 세션에서 추가 갭을 발견했다:

- `.codex/hooks.json`의 `UserPromptSubmit` 이벤트 누락 (hook parity contract 위반)
- `.claude/CLAUDE.md`의 스킬 수 불일치 (11 vs 실제 18)
- `stage-authoring-matrix.md`에 7개 신규 스킬의 stage 매핑 누락
- `AGENTS.md` 섹션 3에 스킬 카운트 미명시
- `docs/90.references/README.md`의 Stage Handoff 섹션 누락
- `infra/tech-stack.versions.json` 드리프트 (16개 컴포넌트, Dependabot PR 미반영)
- `docs/90.references/llm-wiki/index.md` 미갱신

## Goals & In-Scope

- **Goals**: GAP-NEW-05~07, 09의 저위험 갭 즉시 클로저; GAP-NEW-03 차단 기록
- **In Scope**: `.codex/hooks.json`, `AGENTS.md`, `stage-authoring-matrix.md`, `docs/90.references/README.md`, `infra/tech-stack.versions.json`, LLM Wiki 재생성

## Non-Goals & Out-of-Scope

- **Non-goals**: Docker 런타임 동작 변경, 시크릿 값 변경, `.env` 값 변경
- **Out of Scope**: GAP-NEW-08(ops 고아 파일 분류), GAP-NEW-10(pre-commit 통합) — 중간/고위험으로 deferred

## Work Breakdown

| Task              | Description                           | Files / Docs Affected                  | Validation Criteria                  |
| ----------------- | ------------------------------------- | -------------------------------------- | ------------------------------------ |
| PLN-001           | `UserPromptSubmit` hook parity 추가   | `.codex/hooks.json`                    | 7개 이벤트 모두 존재, JSON 유효      |
| PLN-002           | 스킬 카운트 명시                      | `AGENTS.md`                            | "18 skills" 문자열 존재              |
| PLN-003           | Stage Authoring Matrix 스킬 섹션 추가 | `stage-authoring-matrix.md`            | Section 4 존재, 7개 스킬 매핑        |
| PLN-004           | 90.references Stage Handoff 섹션 추가 | `docs/90.references/README.md`         | "Stage Handoff" 섹션 존재            |
| PLN-005           | tech-stack 드리프트 정정              | `infra/tech-stack.versions.json`       | `check-repo-contracts.sh` failures=0 |
| PLN-006           | LLM Wiki 인덱스 재생성                | `docs/90.references/llm-wiki/index.md` | `check-repo-contracts.sh` failures=0 |
| PLN-007 (BLOCKED) | `.claude/CLAUDE.md` 스킬 수 수정      | `.claude/CLAUDE.md`                    | 차단됨 — 사용자 수동 수정 필요       |

## Verification Plan

| ID      | Level      | Description                     | Command / How to Run                                 | Pass Criteria            |
| ------- | ---------- | ------------------------------- | ---------------------------------------------------- | ------------------------ | ----------- |
| VAL-001 | Structural | repo contracts                  | `bash scripts/validation/check-repo-contracts.sh`    | failures=0               |
| VAL-002 | Structural | doc traceability                | `bash scripts/validation/check-doc-traceability.sh`  | failures=0               |
| VAL-003 | Structural | Compose validation              | `bash scripts/validation/validate-docker-compose.sh` | No errors                |
| VAL-004 | Structural | UserPromptSubmit in Codex hooks | `jq '.hooks                                          | keys' .codex/hooks.json` | 7개 키 확인 |

## Risks & Mitigations

| Risk                                   | Impact | Mitigation                                                   |
| -------------------------------------- | ------ | ------------------------------------------------------------ |
| `.claude/CLAUDE.md` 자기-수정 차단     | Low    | GAP-NEW-03 블록 기록, 사용자에게 수동 수정 안내              |
| tech-stack.versions.json 드리프트 재발 | Medium | Dependabot PR merge 시 JSON 수동 갱신 필요 — future ADR 권장 |

## Completion Criteria

- [x] GAP-NEW-05: stage-authoring-matrix.md Section 4 추가
- [x] GAP-NEW-06: AGENTS.md 스킬 카운트 명시
- [x] GAP-NEW-07: 90.references Stage Handoff 섹션 추가
- [x] GAP-NEW-09: `.codex/hooks.json` UserPromptSubmit 추가
- [x] tech-stack 드리프트 클로저 (PLN-005, PLN-006)
- [ ] GAP-NEW-03: `.claude/CLAUDE.md` 수동 수정 (사용자 pending)
- [ ] GAP-NEW-08 (deferred): ops 고아 파일 tier 분류 문서화
- [ ] GAP-NEW-10 (deferred): pre-commit 검증 스크립트 통합

## Related Documents

- **Previous Audit Plan**: [2026-05-26-workspace-audit](./2026-05-26-workspace-audit.md)
- **Previous Audit Task**: [2026-05-26-workspace-audit task](../tasks/2026-05-26-workspace-audit.md)
- **Gap Closure Task**: [2026-05-26-workspace-audit-gap-closure task](../tasks/2026-05-26-workspace-audit-gap-closure.md)
- **Operations**: [Operations index](../../05.operations/README.md)
