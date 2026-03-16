---
goal: 'Standardize documentation and implement Lazy Loading for AI instructions.'
version: '1.0'
date_created: '2026-03-16'
last_updated: '2026-03-16'
owner: 'buenhyden'
status: 'Planned'
scope: 'master'
tags: ['implementation', 'planning']
stack: 'markdown'
layer: 'plans'
---

# Documentation Reorganization and Instruction Optimization Plan

> **Status**: Planned
> **Scope**: master
> **layer:** plans

**Overview (KR):** 본 계획은 저장소의 문서를 재조직하고 에이전트 지침을 최적화하기 위한 구체적인 작업 단계를 정의합니다. `docs/plans/`를 `docs/plans/`으로 변경하고 루트 문서를 보완하는 과정을 포함합니다.

## Context & Introduction

This work exists to align the repository with the [March 2026 Standard] and the user's specific path requirements. It resolves performance issues by modularizing AI context.

## Tasks

| Task     | Description                                     | Files Affected                               | Target REQ     | Validation Criteria            |
| -------- | ----------------------------------------------- | -------------------------------------------- | -------------- | ------------------------------ |
| TASK-001 | Promote contributing/collaboration docs to root | `CONTRIBUTING.md`, `COLLABORATING.md`        | REQ-PRD-006    | Files exist in root            |
| TASK-002 | Rename `docs/plans/` to `docs/plans/`            | `docs/plans/` -> `docs/plans/`                | REQ-PRD-003    | Directory renamed, links fixed |
| TASK-003 | Update `docs/agentic/` for Lazy Loading         | `gateway.md`, `instructions.md`, `rules/`    | REQ-PRD-004/05 | Token count < 15k              |
| TASK-004 | Standardize Frontmatter and Overview (KR)       | All `docs/**/*.md`                           | REQ-PRD-001/02 | Audit script passes            |
| TASK-005 | Update root documents (`README`, `ARCH`, etc.)  | `README.md`, `ARCHITECTURE.md`               | REQ-PRD-002/06 | Links and metadata updated     |

## Verification

- `[VAL-001]` Run `ls -R docs/` to verify folder structure.
- `[VAL-002]` Execute `grep -L "layer:" docs/**/*.md` to find missing metadata.
- `[VAL-003]` Check `gateway.md` markers match rule filenames.

## References

- `../prd/2026-03-16-documentation-standardization-prd.md`
- `../specs/2026-03-16-documentation-refactor-spec.md`
- `../ard/documentation-system-ard.md`
- `../adr/0026-documentation-structure-and-lazy-loading.md`
