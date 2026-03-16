---
goal: 'Implement intent-based agent rules and refine doc paths'
version: '1.0'
date_created: '2026-03-15'
last_updated: '2026-03-15'
owner: 'buenhyden'
status: 'Planned'
scope: 'master'
tags: ['implementation', 'planning']
layer: agentic
---

# Agent Rule Implementation and Refactor Plan

> **Status**: Planned
> **Scope**: master
> **layer:** product

**Overview (KR):** 본 계획은 루트 지침 파일에 규칙 자동 로딩 기능을 추가하고, 저장소의 모든 관리 문서와 지침 파일을 새로운 구조에 맞춰 최종적으로 완성하는 실행 단계를 다룹니다.

## Context & Introduction

This is the final execution phase for the refactoring task initiated in the previous cycle. It focuses on the high-level entrypoints (`AGENTS.md`, etc.).

## Tasks

| Task     | Description                                         | Files Affected                       | Target REQ   | Validation Criteria          |
| -------- | --------------------------------------------------- | ------------------------------------ | ------------ | ---------------------------- |
| TASK-006 | Update `AGENTS.md` with rule trigger matrix         | `AGENTS.md`                          | REQ-RULE-01  | `[LOAD:RULES:*]` present     |
| TASK-007 | Update `GEMINI.md` with rule triggers               | `GEMINI.md`                          | REQ-RULE-01  | Consistent with AGENTS.md    |
| TASK-008 | Update `CLAUDE.md` metadata and shim links          | `CLAUDE.md`                          | REQ-RULE-02  | Imports valid guides         |
| TASK-009 | Refine `docs/agentic/instructions.md` (autonomy)    | `docs/agentic/instructions.md`       | REQ-RULE-03  | Skill clause present         |
| TASK-010 | Final path correction and link audit                | `README.md`, `OPERATIONS.md`         | REQ-RULE-04  | All links point to correct   |

## Verification

- `[VAL-004]` Run integrity check runbook.
- `[VAL-005]` Verify triggers load actual files in `docs/agentic/rules/`.
- `[VAL-006]` Verify `layer` in all newly created PRD/ARDs.

## References

- `[../prd/2026-03-15-rule-implementation-prd.md]`
- `[../ard/2026-03-15-doc-taxonomy-ard.md]`
- `[../adr/0020-intent-based-triggers.md]`
